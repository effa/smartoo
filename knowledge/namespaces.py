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
