# encoding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property

from abstract_component.models import Component
#from common.utils.http import iri2uri
from common.utils.metrics import euclidian_length, sigmoid
from common.utils.wiki import uri_to_name
from common.fields import DictField
from common.settings import ONLINE_ENABLED
from knowledge.fields import GraphField, TermField
from knowledge.namespaces import NAMESPACES_DICT, RDF, RDFS, ONTOLOGY, SMARTOO, TERM
from knowledge.utils.terms import bulk_create_terms_trie, name_to_term  # , term_to_name
from knowledge.utils.text import shallow_parsing, shallow_parsing_phrases, terms_inference
from knowledge.utils.sparql import retrieve_graph_from_dbpedia

from rdflib import Graph, URIRef
from collections import defaultdict
from wikipedia.exceptions import WikipediaException
#from nltk import ParentedTree
import wikipedia
import logging
import traceback


logger = logging.getLogger(__name__)


class KnowledgeBuilder(Component):
    """
    Model for knowledge builder component.
    """

    BEHAVIORS_PATH = 'knowledge/knowledge-builder-behaviors/'

    @classmethod
    def get_behaviors_path(cls):
        return cls.BEHAVIORS_PATH

    def build_knowledge(self, topic):
        """
        Creates (and stores) knowledge graph for given topic.

        Args:
            topic: topic for which to build the knowledge graph
        Raises:
            IntegrityError: if this knowledge builder is not already in DB
                (its ID is needed to store the graph)
            ValueError: if the topic is invalid (there is no such topic)
        """
        # TODO: odstranit toto cachovani behem vyvoje, lepe prepisovat
        # existujici graf
        # At first check if the knowledge graph hasn't already been created
        # (for this builder-topic combo)
        if KnowledgeGraph.objects.filter(topic=topic,
                knowledge_builder=self).exists():
            return  # already created, nothing to do

        try:
            behavior = self.get_behavior()
        except Exception:
            logger.error('Unable to get behavior.')
            raise

        try:
            article = Article.objects.get(topic=unicode(topic))
            #article = Article.objects.get(topic=topic.encode('utf-8'))
        except ObjectDoesNotExist:
            message = 'No article for the topic: {topic}'.format(topic=unicode(topic))
            logger.warning(message)
            raise ValueError(message)

        try:
            knowledge_graph = behavior.build_knowledge_graph(article)
        except ValueError:
            logger.warning('ValueError on knowledge building.')
            raise

        knowledge_graph.knowledge_builder = self
        knowledge_graph.topic = topic
        knowledge_graph.save()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<KnowledgeBuilder {name}; parameters={parameters}>'.format(
            name=self.behavior_name,
            parameters=self.parameters)


# ----------------------------------------------------------------------------
#  Corpora Related
# ----------------------------------------------------------------------------

def article_search(search_string):
    """
    Check if the article for this string is already in DB.
    If not, try to find it on the Wikipedia.
    If it does not exist, raise ValueError

    Returns: topic of the article
    """
    # first try -- search string is exactly name of an article in DB
    try:
        topic = name_to_term(search_string)
        Article.objects.get(topic=topic)
        return topic
    except ValueError:
        pass  # it just means the search_string is not valid part of topic uri
    except ObjectDoesNotExist:
        pass  # it just means the search_string is not a topic in DB

    try:
        assert ONLINE_ENABLED
        # search string normalization
        # replace _ with ' ' (necessary for search to work correctly)
        search_string = search_string.replace('_', ' ')
        wiki_page = wikipedia.page(title=search_string)
        topic = name_to_term(wiki_page.title)
        # check that this is not already in the DB (because of auto-suggest
        # feature, this topic can differ from the originial search_string
        try:
            Article.objects.get(topic=topic)
            # article exist, just return its topic
            return topic
        except ObjectDoesNotExist:
            # create new artcile from retrieved page
            article = Article(topic=topic)

            text = wiki_page.content
            # Problem je, ze seznam odkazu nebude uplny, pokud jich je hodne :-(
            # viz https://github.com/goldsmith/Wikipedia/issues/71
            # patch vysvetlen tady: https://github.com/goldsmith/Wikipedia/pull/80
            # TODO: opravit chybu ve Wikipedia modulu
            links = wiki_page.links

            # make sure title is in the links and in the first position (so it has
            # the highest priority during terms inference
            links.insert(0, wiki_page.title)
            article.create_content_from_text(text, links)
            # save created article and return the topic
            article.save()
            return topic

    except WikipediaException as exc:
        logger.warning(exc.message or 'wiki page retrieval failed')
        raise ValueError('Invalid topic: {topic}'
            .format(topic=unicode(search_string)))


class Article(models.Model):
    """
    Model of article on the English Wikipedia.

    An article is represented as a list of sentences,
    each sentence is represented as a tree (nltk.Tree),
    where internal nodes are chunks (e.g. named entities)
    and leaves are tokens, stored as a tuple (word, pos-tag).

    Attributes:
    _sentences: list of sentences in the article (each sentence is a tree)
    #_terms: dictionary mapping terms to their occurrences in the article
    _terms: set of terms which are in the article

    Each sentence is a ParentedTree, where a node is represented as a list of
    descenants with some additional attributes, such as label (e.g. "S", "VBD",
    "DT", "TERM", "DATE", "PERSON") and (optional) term (URIRef) or literal.
    Example:

    (S
        (PERSON
            (NP Abraham/NP/Abraham-n)
            (NP Lincoln/NP/Lincoln-n)
            .term=URIRef('http://dbpedia.org/resource/Abraham_Lincoln'))
        (VBD was/VBD/be-v)
        (DT the/DT/the-x)
        (TERM
            (CD 16/CD/16-x)
            (NN th/NN/th-n)
            (NN president/NN/president-n)
            (IN of/IN/of-i)
            (DT the/DT/the-x)
            (NP United/NP/United-n)
            (NPS States/NPS/States-n)
            .term=URIRef('http://dbpedia.org/resource/List_of_USA_presidents'))
        (SENT ./SENT/.-x))

    Instead of term attribute, the can also be literal, e.g:
        .literal=Literal('1809-02-12',datatype=XSD.date)},
    """
    # URI of the topic
    # NOTE that it can be different from article URL (e.g.
    # topic=http://dbpedia.org/resource/Abraham_Lincoln
    # but article_url=http://en.wikipedia.org/wiki/Abraham_Lincoln)
    # TODO: if article URL is needed as well, than make an attribute for it
    topic = TermField(unique=True)

    # article content will be stored directly in relational DB encoded in JSON
    content = DictField(default=dict)

    # constant for an empty content
    EMPTY_CONTENT = '{"sentences": [], "terms": []}'

    # weight of the headline (i.e. topic term) relative to one term occurence
    HEADLINE_WEIGHT = 10

    #def save(self, *args, **kwargs):
    #    """
    #    Save modification: if it hasn't been stored already
    #    and content is not set, find the content using Wikipedia API
    #    """
    #    if not self.pk and not self.content:
    #        # find article on Wiki and process it to vertical
    #        try:
    #            self.get_content_from_wikipedia()
    #        except Exception as exc:
    #            logger.error('Wikipedia article processing failed: ' + exc.message)
    #            raise
    #    super(Article, self).save(*args, **kwargs)

    #def get_content_from_wikipedia(self):
    #    """
    #    Uses Wikipedia api to retrieve content for topic of the article
    #    TODO: vyhodit vyjimku, pokud se to nepodari (clanek neexistuje)

    #    Raises:
    #        WikipediaException (see Wikipedia module docs for details)
    #    """
    #    # topic has to be set, content not and online access hat to be enabled
    #    assert self.topic is not None
    #    assert not self.content
    #    assert ONLINE_ENABLED

    #    #print 'simulate wikipedia api .....'
    #    #text = 'Abraham Lincoln was a president of the USA. He led the USA through its Civil war.'
    #    #links = ['Abraham Lincoln', 'USA', 'Civil war']

    #    topic_name = term_to_name(self.topic)

    #    logger.info('online access - Wikipedia: {topic}'.format(topic=topic_name))
    #    try:
    #        #name_utf = topic_name.encode('utf-8')
    #        #wiki_page = wikipedia.page(name_utf)
    #        wiki_page = wikipedia.page(topic_name)
    #    except WikipediaException as exc:
    #        logger.warning(exc.message or 'wiki page retrieval failed')
    #        raise

    #    text = wiki_page.content
    #    # Problem je, ze seznam odkazu nebude uplny, pokud jich je hodne :-(
    #    # viz https://github.com/goldsmith/Wikipedia/issues/71
    #    # patch vysvetlen tady: https://github.com/goldsmith/Wikipedia/pull/80
    #    # TODO: opravit chybu ve Wikipedia modulu
    #    links = wiki_page.links

    #    # make sure title is in the links and in the first position (so it has
    #    # the highest priority during terms inference
    #    links.insert(0, topic_name)
    #    self.create_content_from_text(text, links)

    # TODO: da se to urcite udelat lip (efektivneji, prehledneji), v nltk
    # je primo nejaka prace s texty jako soubory vet, nebo dokonce i
    # korpusy (i oznackovanymi korpusy!)
    def create_content_from_text(self, text, links=[]):
        """
        Parses text and creates self.content
        """
        sentences = shallow_parsing(text)
        terms = shallow_parsing_phrases(links)
        self.content = {
            'sentences': sentences,
            'terms': zip(links, terms)
        }

    @cached_property
    def sentences(self):
        """
        List of sentences in the article.
        Each sentence is represented as a tree.
        """
        return self.parse_terms_and_sentences(return_sentences=True)

    @cached_property
    def terms_positions(self):
        """
        Dictionary mapping terms to their positions in sentences
        """
        return self.parse_terms_and_sentences(return_terms=True)

    @cached_property
    def euclidian_length(self):
        """
        Euclidian length of the article (only terms are counted).
        """
        document_dict = {
            term: self.get_term_count(term) for term in self.get_all_terms()}
        return euclidian_length(document_dict)

    def parse_terms_and_sentences(self, return_terms=False, return_sentences=False, knowledge_graph=None):
        """
        Parses sentences and terms from content (in json).
        """
        # content must be set before
        assert self.content is not None

        #if 'sentences' not in self.content:
        #    return []

        # vytvoreni TermsTrie ze vsech pojmu
        terms_trie = bulk_create_terms_trie(self.content['terms'], knowledge_graph)

        sentences, terms_positions = terms_inference(self.content['sentences'], terms_trie)

        # set both self.sentences and self.terms_positions
        self.sentences = sentences
        self.terms_positions = terms_positions

        # return what was requested
        if return_terms and return_sentences:
            return terms_positions, sentences
        elif return_terms:
            return terms_positions
        elif return_sentences:
            return sentences

    def get_name(self):
        """
        Returns the name of the topic.
        """
        return uri_to_name(self.topic)

    def get_all_terms(self):
        """
        Returns set of all terms in the article.
        """
        return set(self.terms_positions.keys())

    def get_term_positions(self, term):
        """
        Returns list of positions of :term: in the sentences
        """
        return self.terms_positions[term]

    def get_term_count(self, term):
        """
        Returns number of occurences of given term in the article
        """
        occurences = len(self.get_term_positions(term))
        if term == self.topic:
            occurences += self.HEADLINE_WEIGHT
        return occurences

    def get_sentences(self):
        """
        Returns list of sentences in the article.
        """
        return self.sentences

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<Article: {name}>'.format(name=self.get_name())


# ----------------------------------------------------------------------------
#  Knowledge Representation
# ----------------------------------------------------------------------------

# NOTE: For simplicity of development, the knowledge graph for each topic are
# completely disjoint and stored in relational DB as a serialized string.
# In the futrue we will use some tripplestore, such as Virtuoso.

def get_initialized_graph():
    """
    Returns an empty graph with initialized namespace bindings
    """
    graph = Graph()
    # bind prefixes to common namespaces
    for prefix, namespace in NAMESPACES_DICT.items():
        graph.bind(prefix, namespace)
    return graph


class KnowledgeGraph(models.Model):
    # knowledge graph is determined by KnowledgeBuilder + topic URI
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    topic = TermField()

    # topic + builder should be unique (and with index)
    class Meta:
        unique_together = ("topic", "knowledge_builder")

    # graph representation
    graph = GraphField(default=get_initialized_graph)

    _CACHED_ATTRIBUTES = ['terms_of_type', 'types_of_term', 'all_terms']

    def _update_notification(self):
        # after an update, we may need to recompute some attributes
        # (NOTE: ale mozna by stacilo jen pri pridani RDF["type"])
        # NOTE: using self.__dict__.pop('attribute', None) rather than if
        # self.attribut: del self.attribute, because the latter requires
        # computation of attribute if it is not cached.
        for attribute in self._CACHED_ATTRIBUTES:
            self.__dict__.pop(attribute, None)

    def add(self, triple):
        """
        Adds new triple to knowledge graph.
        """
        self.graph.add(triple)
        # TODO: misto notifikace a nasledneho kompletniho prepocitani vsech
        # cachovanych atributu by slo i pouze upravit jejich hodnoty podle
        # pridaneho tripletu (-> mnohem rychlejsi)
        self._update_notification()

    # TODO: vyfaktorovat implicitni hodnoty parametru do nejakych konstant, aby
    # se dalo lepe rict DEFAULT + neco dalsiho
    def add_related_global_knowledge(self, article,
            predicates=[RDFS['label'], RDF['type'], ONTOLOGY['birthYear'],
                ONTOLOGY['deathYear'], RDFS['comment']], online=True):
        """
        Adds triples from global knowledge which relates to the given article.
        Specifically, adds all terms from the article and all terms one hop
        from the global knowledge graph.

        Args:
            article: for which article to find related global knowledge
            predicates: triples with which predicates to incorporate
        """
        try:
            # at first find all related terms
            terms = article.get_all_terms()
            topic = article.topic
            global_knowledge = GlobalKnowledge()
            primary_graph = global_knowledge.get_graph(topic, online=online)
            if primary_graph:
                terms.update(primary_graph.all_terms)

            for term in terms:
                # add the term in graph
                self.add((term, RDF['type'], SMARTOO['term']))
                secondary_graph = global_knowledge.get_graph(term, online=online)

                if not secondary_graph:
                    continue

                for predicate in predicates:
                    for value in secondary_graph.get_objects(term, predicate):
                        self.add((term, predicate, value))

            self._update_notification()
        except ValueError:
            #logger.error('ValueError: ' + unicode(article.topic) + '\n' + traceback.f)
            logger.error(traceback.format_exc())
            raise

    # TODO: cachovani dotazu (pozor na add())
    def query(self, query, initBindings={}):
        """
        Performs SPARQL query over the knowledge graph.

        Args:
            query: prepared query
            bindings: dictionary of bindings for prepared query
        Returns:
            result set
        """
        return self.graph.query(query, initBindings=initBindings)

    def label(self, uri, fallback_guess=True):
        """
        Returns label for given uri reference stated in the graph.

        Args:
            uri: URI reference to the object for which to find label
            fallback_guess: guess the label (using URI) if label wasn't found
        Returns:
            label [unicode]
        """
        result = self.graph.label(uri)
        if result:
            return unicode(result)
        elif fallback_guess:
            return uri_to_name(uri)
        else:
            return None

    def types(self, term):
        """
        Returns set of types for given term.

        Args:
            term: URI reference to the object for which to find types
        Returns:
            set of types (each type is URIRef)
        """
        assert isinstance(term, URIRef)
        # NOTE: we will use cached dictionary of types
        #result = set(self.graph.objects(subject=term, predicate=RDF['type']))
        # return a shallow copy of the types set
        result = set(self.types_of_term[term])
        return result

    def similarity(self, term1, term2):
        """
        Measures the similarity between two terms in the knowledge graph
        (using metrics based on common types). If one of the terms is not the
        graph, returns 0.

        Returns:
            similarity (real  number between 0 and 1)
        """
        term1_types = self.types(term1)
        term2_types = self.types(term2)
        common_types = term1_types & term2_types
        # don't count smartoo:term and dbpedia:Thing as common types
        common_types_count = len(common_types)

        # normalization -> number between 0 and 1
        # NOTE: devide common_types_count to make the function increse slower
        similarity = 2.0 * (sigmoid(common_types_count / 4.0) - 0.5)
        return similarity

    @cached_property
    def types_of_term(self):
        """
        Mapping from terms to a set of their types (each type is URIRef).
        """
        types_dict = defaultdict(set)
        for term, type_uri in self.graph.subject_objects(predicate=RDF['type']):
            types_dict[term].add(type_uri)
        return types_dict

    @cached_property
    def terms_of_type(self):
        """
        Mapping form types to all terms of that type (in the graph).
        """
        terms_dict = defaultdict(set)
        for term, type_uri in self.graph.subject_objects(predicate=RDF['type']):
            terms_dict[type_uri].add(term)
        return terms_dict

    # if it's used often, consider caching (@cached_property etc.)
    @property
    def all_terms(self):
        """
        Set of all terms in the knowledge graph.

        As terms are consider all subjects/objects in the TERM namespace.
        """
        terms = set()
        term_prefix = unicode(TERM)
        # NOTE: Graph.all_nodes() iterates through all subjects and objects
        for node in self.graph.all_nodes():
            if isinstance(node, URIRef) and node.startswith(term_prefix):
                terms.add(node)

        ## NOTE: Previously, we have considered as terms only subjects with
        ## type "smartoo:term".
        #terms = set(self.graph.subjects(RDF['type'], SMARTOO['term']))

        return terms

    def get_subjects(self, predicate=None, object=None):
        return list(self.graph.subjects(predicate, object))

    def get_objects(self, subject=None, predicate=None):
        return list(self.graph.objects(subject, predicate))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'builder: {builder}\ntopic: {topic}\ngraph:\n{graph}'.format(
            builder=self.knowledge_builder if self.knowledge_builder_id is
            not None else '---',
            topic=self.topic if self.topic is not None else '---',
            graph=self.graph.serialize(format='turtle').decode('utf-8'))


# ----------------------------------------------------------------------------
#   Global Knowledge
# ----------------------------------------------------------------------------

class GlobalKnowledge(object):
    BEHAVIOR_NAME = 'global-knowledge'

    def __init__(self):
        # we don't need knowledge builder to build anything, but we need it as
        # an identifier for knowledge graphs which belongs to global knowledge
        self.knowledge_builder = self._get_global_knowledge_builder()

    def _get_global_knowledge_builder(self):
        """
        Returns the global knowledge builder. If not already exists, then
        create and store it.
        """
        try:
            return KnowledgeBuilder.objects.get(behavior_name=self.BEHAVIOR_NAME)
        except ObjectDoesNotExist:
            # create global knowledge builder
            return KnowledgeBuilder.objects.create(
                behavior_name=self.BEHAVIOR_NAME,
                parameters={})

    def get_graph(self, term, online=True):
        """
        Returns graph for the given term. If not already stored in DB, uses
        public endpoint to get it (if :online: is True) and stores it.

        Args:
            term: URI of the topic term [URIRef]
            online: if graph is not in DB, should it get on the web? [bool]
        Returns:
            knowledge graph
        """
        #if isinstance(term, unicode):
        #    term = URIRef(term)
        assert isinstance(term, URIRef)

        try:
            knowledge_graph = KnowledgeGraph.objects.get(topic=unicode(term).encode('utf-8'),
                knowledge_builder=self.knowledge_builder)
            return knowledge_graph
        except ObjectDoesNotExist:
            if online:
                # use public endpoint to retrieve the graph
                graph = retrieve_graph_from_dbpedia(term)

                # store created graph in DB
                try:
                    knowledge_graph = KnowledgeGraph.objects.create(
                        knowledge_builder=self.knowledge_builder,
                        topic=term,
                        graph=graph)
                except Exception:
                    logger.error('retrieve_graph_from_dbpedia failed\n' + traceback.format_exc())
                    return None

                return knowledge_graph
            else:
                return None

        except Exception as exc:
            logger.error('Getting graph for {term} failed; {message}; {excType}'
                .format(term=term, message=exc.message, excType=unicode(type(exc))))
            return None

    #def label(self, term, fallback_guess=True):
    #    """
    #    Returns label for given term.

    #    Args:
    #        term: URI reference to the object for which to find label
    #        fallback_guess: guess the label (using URI) if label wasn't found
    #    Returns:
    #        label [unicode]
    #    """
    #    # TODO: osetrit neexistenci grafu
    #    graph = self.get_graph(term)
    #    return graph.label(term)

    # NOTE: vzhledem k zvolene zjednodusene reprezentaci globalnich znalosti,
    # nelze v obecnosti implementovat metodu query(sparql), ale pro nase ucely
    # to asi nevadi, nam staci vzdy informace o konkretnim subjetku (napr. jeho
    # typ, datum narozeni atp.)
