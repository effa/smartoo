# encoding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property
from abstract_component.models import Component
from common.utils.wiki import uri_to_name
from knowledge import Article
from knowledge.fields import GraphField
from knowledge.namespaces import NAMESPACES_DICT, RDF, RDFS, FOAF, ONTOLOGY
from knowledge.utils.sparql import ALL_TERMS_QUERY
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

    def build_knowledge(self, topic_uri):
        """
        Creates (and stores) knowledge graph for given topic.

        Args:
            topic_uri: topic for which to build the knowledge graph
        Raises:
            IntegrityError: if this knowledge builder is not already in DB
                (its ID is needed to store the graph)
        """
        # At first check if the knowledge graph hasn't already been created
        # (for this builder-topic combo)
        if KnowledgeGraph.objects.filter(topic_uri=topic_uri,
                knowledge_builder=self).exists():
            return  # already created, nothing to do
        behavior = self.get_behavior()
        # TODO: osetrit neexistenci vertikalu
        vertical = Vertical.objects.get(topic_uri=topic_uri)
        article = vertical.get_article()
        knowledge_graph = behavior.build_knowledge_graph(article)
        knowledge_graph.knowledge_builder = self
        knowledge_graph.topic_uri = topic_uri
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
    # URI of the topic (same as the URL of the corresponding article)
    topic_uri = models.CharField(max_length=120, unique=True)

    # vertical for the topic will be stored directly in our relational DB
    content = models.TextField()

    def get_name(self):
        """
        Returns the name of the topic.
        """
        return uri_to_name(self.topic_uri)

    def get_article(self):
        """
        Returns article for given topic

        Returns:
            article instance (knowledge.Article)
        """
        return Article(uri=self.topic_uri, vertical=self.content)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<Vertical uri="{uri}">'.format(uri=self.topic_uri)


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
    topic_uri = models.CharField(max_length=120)

    # graph representation
    graph = GraphField(default=get_initialized_graph)

    # TODO: definovat unikatnost dvojice KB-topic a zajistit, aby se graf pro
    # takovou dvojici nevytvarel znova

    # TODO: define access methods to work with the knowledge graph

    def _update_notification(self):
        # after an update, we may need to recompute some attributes
        # (NOTE: ale mozna by stacilo jen pri pridani RDF["type"])
        if self.terms_of_type:
            del self.terms_of_type
        if self.types_of_term:
            del self.types_of_term

    def add(self, triple):
        """
        Adds new triple to knowledge graph.
        """
        self.graph.add(triple)
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
        # TODO: misto SPARQL dotazu by stacilo pouzit graph.value(), reps. dokonce
        # existuje Graph.label() nebo Graph.preferredLabel()
        #result = graph.query(LABEL_QUERY, initBindings={'uri': uri})
        #try:
        #    return unicode(next(iter(result))[0])
        #except StopIteration:
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
        # normalization -> number between 0 and 1)
        similarity = 1 - (1.0 / (len(common_types) + 1))
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

    def get_all_terms(self, types_dict=False):
        # TODO: umoznit vracet slovnik mapovani pojmu na typy
        terms = set()
        for result in self.query(ALL_TERMS_QUERY):
            terms.add(result[0])
        return terms

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'builder: {builder}\ntopic: {topic}\ngraph:\n{graph}'.format(
            builder=self.knowledge_builder if self.knowledge_builder_id is
            not None else '---',
            topic=self.topic_uri if self.topic_uri is not None else '---',
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
        assert isinstance(term, URIRef)
        try:
            knowledge_graph = KnowledgeGraph.objects.get(topic_uri=term,
                knowledge_builder=self.knowledge_builder)
            return knowledge_graph

        except ObjectDoesNotExist:
            if not online:
                return None

            # use public endpoint to retrieve the graph
            graph = Graph()
            graph.parse(term)
            # TODO: osetrit neexistenci grafu na danem zdroji

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
                topic_uri=term,
                graph=filtered_graph)

            return knowledge_graph

    def label(self, uri, fallback_guess=True):
        """
        Returns label for given uri reference.

        Args:
            uri: URI reference to the object for which to find label
            fallback_guess: guess the label (using URI) if label wasn't found
        Returns:
            label [unicode]
        """
        # TODO: osetrit neexistenci grafu
        graph = self.get_graph(uri)
        return graph.label(uri)

    # NOTE: vzhledem k zvolene zjednodusene reprezentaci globalnich znalosti,
    # nelze v obecnosti implementovat metodu query(sparql), ale pro nase ucely
    # to asi nevadi, nam staci vzdy informace o konkretnim subjetku (napr. jeho
    # typ, datum narozeni atp.)
