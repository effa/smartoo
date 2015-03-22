# encoding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property

from abstract_component.models import Component
from common.utils.http import iri2uri
from common.utils.metrics import euclidian_length, sigmoid
from common.utils.wiki import uri_to_name
from common.fields import DictField
from common.settings import ONLINE_ENABLED
from knowledge.fields import GraphField, TermField
from knowledge.namespaces import NAMESPACES_DICT, RDF, RDFS, FOAF, ONTOLOGY, SMARTOO, TERM
from knowledge.utils.terms import bulk_create_terms_trie, term_to_name
from knowledge.utils.text import shallow_parsing, shallow_parsing_phrases, terms_inference

from rdflib import Graph, URIRef
from collections import defaultdict
#from nltk import ParentedTree
import wikipedia


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

        behavior = self.get_behavior()

        try:
            article = Article.objects.get(topic=topic)
        except ObjectDoesNotExist:
            raise ValueError('Invalid topic: {topic}'
                .format(topic=unicode(topic)))

        knowledge_graph = behavior.build_knowledge_graph(article)
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

    def save(self, *args, **kwargs):
        """
        Save modification: if it hasn't been stored already
        and content is not set, find the content using Wikipedia API
        """
        if not self.pk and not self.content:
            # find article on Wiki and process it to vertical
            self.get_content_from_wikipedia()

        super(Article, self).save(*args, **kwargs)

    def get_content_from_wikipedia(self):
        """
        Uses Wikipedia api to retrieve content for topic of the article
        TODO: vyhodit vyjimku, pokud se to nepodari (clanek neexistuje)

        Raises:
            WikipediaException (see Wikipedia module docs for details)
        """
        # topic has to be set, content not and online access hat to be enabled
        assert self.topic is not None
        assert not self.content
        assert ONLINE_ENABLED
        # TODO: log 'Wikipedia access'

        #print 'simulate wikipedia api .....'
        #text = 'Abraham Lincoln was a president of the USA. He led the USA through its Civil war.'
        #links = ['Abraham Lincoln', 'USA', 'Civil war']

        topic_name = term_to_name(self.topic)

        wiki_page = wikipedia.page(topic_name)

        text = wiki_page.content
        # Proble je, ze seznam odkazu nebude uplny, pokud jich je hodne :-(
        # viz https://github.com/goldsmith/Wikipedia/issues/71
        # patch vysvetlen tady: https://github.com/goldsmith/Wikipedia/pull/80
        # TODO: opravit chybu ve Wikipedia modulu
        links = wiki_page.links

        # make sure title is in the links and in the first position (so it has
        # the highest priority during terms inference
        links.insert(0, topic_name)
        self.create_content_from_text(text, links)

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

    # graph representation
    graph = GraphField(default=get_initialized_graph)

    # TODO: definovat unikatnost dvojice KB-topic a zajistit, aby se graf pro
    # takovou dvojici nevytvarel znova

    # TODO: define access methods to work with the knowledge graph

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
        # at first find all related terms
        terms = article.get_all_terms()
        topic = article.topic
        global_knowledge = GlobalKnowledge()
        primary_graph = global_knowledge.get_graph(topic, online=online)
        if primary_graph:
            terms.update(primary_graph.all_terms)

        #i = 2
        for term in terms:
            # add the term in graph
            self.add((term, RDF['type'], SMARTOO['term']))
            secondary_graph = global_knowledge.get_graph(term, online=online)
            #print '#' * 70
            #print 'term:', term
            #print secondary_graph

#            print '#' * 70
#            print """
#  <object pk="{i}" model="knowledge.knowledgegraph">
#    <field to="knowledge.knowledgebuilder" name="knowledge_builder" rel="ManyToOneRel">1</field>
#    <field type="CharField" name="topic">{topic}</field>
#    <field type="TextField" name="graph"><![CDATA[
#{graph}]]>
#    </field>
#  </object>
#""".format(i=i, topic=term, graph=secondary_graph.graph.serialize(format='turtle').decode('utf-8'))
#            i += 1
#            raw_input()

            if not secondary_graph:
                continue

            for predicate in predicates:
                for value in secondary_graph.get_objects(term, predicate):
                    self.add((term, predicate, value))

        self._update_notification()

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
            knowledge_graph = KnowledgeGraph.objects.get(topic=term,
                knowledge_builder=self.knowledge_builder)
            return knowledge_graph

        except ObjectDoesNotExist:
            if not online:
                return None

            assert ONLINE_ENABLED

            # use public endpoint to retrieve the graph
            graph = Graph()

            # TODO: log '(online!) k/models.py,L369, term:', term
            print 'online, k/models.py, L 568', term, type(term), iri2uri(term)
            graph.parse(iri2uri(term))
            # TODO: osetrit neexistenci grafu na danem zdroji
            # except HTTPError

            # namespaces binding
            filtered_graph = Graph()
            for prefix, namespace in NAMESPACES_DICT.items():
                filtered_graph.bind(prefix, namespace)

            # graph filtering
            predicate_namespaces = tuple(unicode(ns) for ns in (FOAF, RDF,
                RDFS, ONTOLOGY))
            for (s, p, o) in graph.triples((term, None, None)):
                # only preserve predicates in "reliable" namespaces
                # and fitler wikiPageRevisionID, wikiPageExternalLike etc.
                if p.startswith(predicate_namespaces) and\
                        not p.startswith(ONTOLOGY['wiki']):
                    # only preserve objects which are not literals in
                    # non-english languages
                    if isinstance(o, URIRef) or not o.language\
                            or o.language == 'en':
                        # if the triple passed all these filteres, add it to
                        # the graph
                        filtered_graph.add((s, p, o))

            # store created (and filtered) graph in DB
            knowledge_graph = KnowledgeGraph.objects.create(
                knowledge_builder=self.knowledge_builder,
                topic=term,
                graph=filtered_graph)

            return knowledge_graph

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
