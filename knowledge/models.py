# encoding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property
from abstract_component.models import Component
from common.utils.wiki import uri_to_name
from knowledge import Article
from knowledge.fields import GraphField, TermField
from knowledge.namespaces import NAMESPACES_DICT, RDF, RDFS, FOAF, ONTOLOGY, SMARTOO, TERM
from rdflib import Graph, URIRef
from collections import defaultdict


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
        """
        # TODO: odstranit toto cachovani behem vyvoje, lepe prepisovat
        # existujici graf
        # At first check if the knowledge graph hasn't already been created
        # (for this builder-topic combo)
        if KnowledgeGraph.objects.filter(topic=topic,
                knowledge_builder=self).exists():
            return  # already created, nothing to do
        behavior = self.get_behavior()
        # TODO: osetrit neexistenci vertikalu
        vertical = Vertical.objects.get(topic=topic)
        article = Article(vertical)
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

class Vertical(models.Model):
    """
    Model for verticals of articles on the English Wikipedia.
    Corresponds to topics which can be practiced.
    """
    # URI of the topic
    # NOTE that it can be different from article URL (e.g.
    # topic=http://dbpedia.org/resource/Abraham_Lincoln
    # but article_url=http://en.wikipedia.org/wiki/Abraham_Lincoln)
    topic = TermField(unique=True)

    # TODO: if article URL is needed as well, than make an attribute for it

    # vertical for the topic will be stored directly in our relational DB
    content = models.TextField()

    def get_name(self):
        """
        Returns the name of the topic.
        """
        return uri_to_name(self.topic)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<Vertical topic="{topic}">'.format(topic=self.topic)


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
        topic = article.get_topic()
        global_knowledge = GlobalKnowledge()
        # online=False is just to make sure test don't use public endpoint,
        # all data should be in fixtures
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
        # all terms should have at least one type (smartoo:term), but if not,
        # just return 0
        if not common_types:
            return 0.0
        # normalization -> number between 0 and 1
        similarity = 1 - (1.0 / len(common_types))
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

            # use public endpoint to retrieve the graph
            graph = Graph()

            print '(online!) k/models.py,L369, term:', term
            graph.parse(term)
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
