from django.db import models
#from rdflib import URIRef


class KnowledgeBuilder(models.Model):
    # TODO: vynutit unique pro code_path
    code_path = models.TextField()
    # parameeters: json (more flexible than relational table for parameters)
    parameters = models.TextField()
    performance = models.FloatField()

# TODO: podobne modely dalsich komponent (v prislusnych balicich)

# NOTE: mozna by bylo flexibilnejsi i usporneji misto tabulky pro parametry
# proste ukladat json parametru primo do hlavni tabulky KnowledgeBuilder
#class KnowledgeBuilderParameter(models.Model):
#    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
#    key = models.CharField(max_length=50)
#    value = models.DecimalField(max_digits=10, decimal_places=10)


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
