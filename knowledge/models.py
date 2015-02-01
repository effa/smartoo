from __future__ import unicode_literals
from abstract_component.models import Component
from common.utils.wiki import uri_to_name
from django.db import models
from rdflib import URIRef, Graph


class KnowledgeBuilder(Component):
    """
    Model for knowledge builder component.
    """

    BEHAVIORS_PATH = 'knowledge/knowledge-builder-behaviors/'
    #BEHAVIOR_CLASS = 'KnowledgeBuilderBehavior'

    @classmethod
    def get_behaviors_path(cls):
        return cls.BEHAVIORS_PATH

    def build_knowledge_graph(self, topic):
        """
        Creates (and stores) knowledge graph for given topic.

        Args:
            topic (knowledge.models.Topic): topic for which to build
                the knowledge graph
        """
        raise NotImplementedError

    def __unicode__(self):
        return '<KnowledgeBuilder {name}>'.format(name=self.name)


# ----------------------------------------------------------------------------
#  Corpora Related
# ----------------------------------------------------------------------------

class Vertical(models.Model):
    """
    Representation of vertical for one article
    """
    # NOTE: ukladat vertikaly do DB (podobne jako grafy), proste to celou vec
    # zjednodusi a opet napsat obalkove metody/neperzistentni atributy
    # (jo a napred zkontrolovat, ze to s temi neperzistentnimi atributy opravdu
    # funguje ... v shellu a taky samozrejme napsat testy ...)
    content = models.TextField()


class Topic(models.Model):
    """
    Model for topics, which can be practiced. Corresponds to the articles
    on the Enlglish Wikipedia.
    """
    # URI of the term (resource) to practice
    # (same as the URL of the corresponding article)
    uri = models.CharField(max_length=120, unique=True)

    # vertical for the topic will be stored directly in our relational DB
    vertical = models.ForeignKey(Vertical)

    # index (start line) of the article in the vertical file
    # (vertical file of English Wikipedia with terms inferred)
    #index = models.BigIntegerField()
    # NOTE: index neni potreba, vertikal bude ulozen primo v DB jako
    # dlouhy string

    def get_name(self):
        """
        Returns the name of the topic.
        """
        return uri_to_name(self.uri)


# ----------------------------------------------------------------------------
#  Knowledge Representation
# ----------------------------------------------------------------------------

# NOTE: For simplicity of development, the knowledge graph for each topic are
# completely disjoint and stored in relational DB as a serialized string.
# In the futrue we will use some tripplestore, such as Virtuoso.

class KnowledgeGraph(models.Model):
    # knowledge graph is determined by KnowledgeBuilder+Topic)
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    topic = models.ForeignKey(Topic)

    # persistent graph representation (TODO: in which format?)
    serialized_graph = models.TextField()

    # non-persistent graph representation (rdflib.Graph)
    graph = Graph()  # Conjunctive Graph, ... ???

    # TODO: define access methods to work with the knowledge graph

    def save(self, *args, **kwargs):
        """
        Serialize the graph and save it.
        """
        # TODO: serialize the graph before saving
        super(KnowledgeGraph, self).save(*args, **kwargs)


class Resource(URIRef):
    """
    For now, this is just an alias for URIRef...
    (But probably I'll write some additional convenience methods later...)
    """
    # NOTE: This is not a model, since (for now) there is no reason to have a
    # table of resource.
    pass
