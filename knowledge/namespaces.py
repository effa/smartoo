from rdflib import Namespace
from rdflib.namespace import FOAF, RDFS, DC, XSD

"""
Module for RDF namespaces.
"""

RESOURCE = Namespace('http://dbpedia.org/resource/')
ONTOLOGY = Namespace('http://dbpedia.org/ontology/')

NAMESPACES_DICT = {
    'dbpedia': RESOURCE,
    'dbpedia-owl': ONTOLOGY,
    'foaf': FOAF,
    'rdfs': RDFS,
    'dc': DC,
    'xsd': XSD
}
