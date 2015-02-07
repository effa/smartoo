from rdflib import Namespace
from rdflib.namespace import FOAF, RDFS, DC, XSD

"""
Module for RDF namespaces.
"""

RESOURCE = Namespace('http://dbpedia.org/resource/')
ONTOLOGY = Namespace('http://dbpedia.org/ontology/')
# own namespaces
SMARTOO = Namespace('http://fi.muni.cz/smartoo/')

NAMESPACES_DICT = {
    'dbpedia': RESOURCE,
    'dbpedia-owl': ONTOLOGY,
    'smartoo': SMARTOO,
    'foaf': FOAF,
    'rdfs': RDFS,
    'dc': DC,
    'xsd': XSD
}
