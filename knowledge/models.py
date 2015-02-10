from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from abstract_component.models import Component
from common.utils.wiki import uri_to_name
from knowledge import Article
from knowledge.fields import GraphField
from knowledge.namespaces import NAMESPACES_DICT
from knowledge.utils.sparql import ALL_TERMS_QUERY
from rdflib import Graph


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

    def add(self, triple):
        """
        Adds new triple to knowledge graph.
        """
        self.graph.add(triple)

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

    def get_all_terms(self, types_dict=False):
        # TODO: umoznit vracet slovnik mapovani pojmu na typy
        terms = set()
        for result in self.query(ALL_TERMS_QUERY):
            terms.add(result[0])
        return terms

    def __unicode__(self):
        return 'builder: {builder}\ntopic: {topic}\ngraph:\n{graph}'.format(
            builder=self.knowledge_builder if self.knowledge_builder_id is
            not None else '---',
            topic=self.topic_uri if self.topic_uri is not None else '---',
            graph=self.graph.serialize(format='turtle'))


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

    def get_graph(self, term):
        """
        Returns graph for the given term. If not already stored in DB, uses
        public endpoint to get it.
        """
        try:
            knowledge_graph = KnowledgeGraph.objects.get(topic_uri=term,
                knowledge_builder=self.knowledge_builder)
            return knowledge_graph
        except ObjectDoesNotExist:
            # use public endpoint to retrieve the graph
            graph = Graph()
            # NOTE: there are literals in all languages -> filtering needed
            graph.parse(term)
            # TODO: filter it (only english literals; discard all unreliable
            # triples (dbprop etc)
            knowledge_graph = KnowledgeGraph.objects.create(
                knowledge_builder=self.knowledge_builder,
                topic_uri=term,
                graph=graph)
            return knowledge_graph

    # NOTE: vzhledem k zvolene zjednodusene reprezentaci globalnich znalosti,
    # nelze v obecnosti implementovat metodu query(sparql), ale pro nase ucely
    # to asi nevadi, nam staci vzdy informace o konkretnim subjetku (napr. jeho
    # typ, datum narozeni atp.)
