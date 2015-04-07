from rdflib import Namespace
from rdflib.namespace import FOAF, RDFS, DC, XSD, RDF
#from common.utils.wiki import uri_to_name

"""
Module for RDF namespaces.
"""

# namespaces
TERM = Namespace('http://dbpedia.org/resource/')
ONTOLOGY = Namespace('http://dbpedia.org/ontology/')
DCTERMS = Namespace('http://purl.org/dc/terms/')
# own namespaces
SMARTOO = Namespace('http://fi.muni.cz/smartoo/')

# mapping of prefixes to namespaces
NAMESPACES_DICT = {
    'dbpedia': TERM,
    'dbpedia-owl': ONTOLOGY,
    'smartoo': SMARTOO,
    'foaf': FOAF,
    'rdf': RDF,
    'rdfs': RDFS,
    'dc': DC,
    'xsd': XSD,
    'dcterms': DCTERMS
}

# preprepared nodes
LABEL = RDFS['label']
TYPE = RDF['type']


# NOTE: Vysvetleni reseni: pri desiralizaci grafu se jsou vsechny uzly URIref,
# takze nikdy nebudou typu Term. Snazit se rozlisit typy pomoci Pythonich trid
# je spatne reseni.

#class Term(URIRef):
#    """
#    Term representation. Term is a special case of URIRef (with RESOURCE
#    namespace), which is itself just a special case of unicode string.
#    """

#    def __new__(cls, term_name):
#        # if the :term_name: starts with RESOURCE prefix, we will use it
#        # directly, otherwise we will add to it the RESOURCE namespace
#        if term_name.startswith(RESOURCE):
#            uri = term_name
#        else:
#            # TODO: there should be probably more transformations (because of URL
#            # encdoing, e.g. "/" etc.)
#            term_name = term_name.replace(' ', '_')
#            uri = RESOURCE + term_name
#        return super(Term, cls).__new__(cls, uri)

#    def get_name(self):
#        return uri_to_name(self)

#    def __eq__(self, other):
#        # NOTE: we want it to be equal to URIRefs
#        return (isinstance(other, URIRef) and unicode(self) == unicode(other))

#    def __ne__(self, other):
#        return not self.__eq__(other)
