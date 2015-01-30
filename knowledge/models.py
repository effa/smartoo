from __future__ import unicode_literals
from abstract_component.models import Component
from common import Topic
from django.db import models
from rdflib import URIRef, Graph


class KnowledgeBuilder(Component):

    def __unicode__(self):
        return '<KnowledgeBuilder {name}>'.format(name=self.name)


# TODO: podobne modely dalsich komponent (v prislusnych balicich)


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


# ----------------------------------------------------------------------------
#  Corpora Related
# ----------------------------------------------------------------------------

class Vertical(models.Model):
    """
    Representation of vertical for one article
    """
    # TODO: ukladat vertikaly do DB (podobne jako grafy), proste to celou vec
    # zjednodusi a opet napsat obalkove metody/neperzistentni atributy
    # (jo a napred zkontrolovat, ze to s tema neperzistentnimi atributy opravdu
    # funguje ... v shellu a taky samozrejme napsat testy ...)
    pass
