"""
Module for knowledge representation.
Definition of entity classes for Term, Triplet and KnowledgeGraph
"""

# Alternativa: proste pouzivat rovnou URIref, trojice a ConjuctiveGraph
# Ale radsi vlastni definice (vice prace, ale moznost zmeni RDF knihovny,
# rozsiritelnost, ...)

from rdflib import URIRef


class Term(object):

    def __init__(self, uri):
        """
        Args:
            uri (unicode)
        """
        self._uri_ref = URIRef(uri)


class Triplet(object):
    pass


class KnowledgeGraph(object):
    pass
