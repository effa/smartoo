from __future__ import unicode_literals
#from django.db import models
from abstract_component.models import Component
#from rdflib import URIRef


class KnowledgeBuilder(Component):

    def __unicode__(self):
        return '<KnowledgeBuilder {name}>'.format(name=self.name)


# TODO: podobne modely dalsich komponent (v prislusnych balicich)
#


# ----------------------------------------------------------------------------
#  Knowledge Representation
# ----------------------------------------------------------------------------

# TODO: Term a Knowledge ???
# Alternativa: proste pouzivat rovnou URIref, trojice a ConjuctiveGraph
# Ale radsi vlastni definice (vice prace, ale moznost zmeni RDF knihovny,
# rozsiritelnost, ...)

#class Term(object):

#    def __init__(self, uri):
#        """
#        Args:
#            uri (unicode)
#        """
#        self._uri_ref = URIRef(uri)


#class Triplet(object):
#    pass


#class KnowledgeGraph(object):
#    pass


# ----------------------------------------------------------------------------
#  Corpora Related
# ----------------------------------------------------------------------------

class Vertical(object):
    """
    Representation of vertical for one article
    """
    pass
