"""
Utilities for SPARQL language
"""

from __future__ import unicode_literals
from common.settings import ONLINE_ENABLED
from knowledge.namespaces import NAMESPACES_DICT, RDF, RDFS, FOAF, ONTOLOGY, DCTERMS
from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph, Literal, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib import quote_plus
from urllib2 import HTTPError

import cjson
import logging
#import traceback


logger = logging.getLogger(__name__)


def prepared_query(query_string):
    """
    Returns prepared query with initialized standard namespaces bindings.
    """
    return prepareQuery(query_string, initNs=NAMESPACES_DICT)


def retrieve_graph_from_dbpedia(term):
    assert ONLINE_ENABLED
    logger.info('online access - DBpedia: {term}'.format(term=unicode(term)))
    term_utf = term.encode('utf-8')
    term_url = quote_plus(term_utf, safe=str("/:,()'"))
    #print '---'
    #print 'term_url', term_url
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    #query = """
    #    SELECT ?p ?o
    #    WHERE {{ <{term_url}> ?p ?o }}
    #""".format(term_url=term_url)
    query = """
        SELECT ?p ?o
        WHERE {{
            <{term_url}> ?p ?o
            FILTER( STRSTARTS(STR(?p), "{foaf}")
                || STRSTARTS(STR(?p), "{rdf}")
                || STRSTARTS(STR(?p), "{rdfs}")
                || STRSTARTS(STR(?p), "{dcterms}")
                || STRSTARTS(STR(?p), "{ontology}"))
            FILTER (isURI(?o) || langMatches(lang(?o), "EN"))
        }}
    """.format(term_url=term_url,
            foaf=unicode(FOAF),
            rdf=unicode(RDF),
            rdfs=unicode(RDFS),
            dcterms=unicode(DCTERMS),
            ontology=unicode(ONTOLOGY))

    sparql.setQuery(query.encode('utf-8'))
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query()
        # workaround for "Invalid \escape" error which can be raised by
        # convert()
        body = results.response.read()
        results = cjson.decode(body)
    except HTTPError as exc:
        # can occur if DBpedia is under maintenance (quite often)
        # TODO: propaget error and show message to the user
        logger.error('Getting graph for {term} failed; {message}; {excType}'
            .format(term=term, message=exc.message, excType=unicode(type(exc))))
        return None

    # create graph and bind relevant namespaces
    graph = Graph()
    for prefix, namespace in NAMESPACES_DICT.items():
        graph.bind(prefix, namespace)

    LITERAL_MAX_LENGTH = 600
    for result in results["results"]["bindings"]:
        try:
            p = URIRef(result['p']['value'])
            # filter wikiPageRevisionID, wikiPageExternalLike etc.
            if p.startswith(ONTOLOGY['wiki']):
                continue
            if result['o']['type'] == 'uri':
                o = URIRef(result['o']['value'])
            else:
                o = Literal(result['o']['value'])
                # if object is too long (e.g. abstract, ignore it)
                if len(o) > LITERAL_MAX_LENGTH:
                    continue
            graph.add((term, p, o))
            #print type(p), p
            #print type(o), o
            #print '*'
        except KeyError:
            continue

    # check if the graph is not empty
    if not graph:
        logger.warning('Retrieved empty graph for ' + unicode(term))

    return graph

# ---------------------------------------------------------------------------
#  preprepared queries
# ---------------------------------------------------------------------------

#LABEL_QUERY = prepared_query("""
#    SELECT ?label
#    WHERE {
#        ?uri rdfs:label ?label
#    }
#""")


#def label(uri, graph, fallback_guess=True):
#    """
#    Returns label for given uri reference stated in the given graph.

#    Args:
#        uri: URI reference to the object for which to find label
#        graph: where to search for the label
#        fallback_guess: guess the label (using URI) if label wasn't found
#    Returns:
#        label [unicode]
#    """
#    # TODO: misto SPARQL dotazu by stacilo pouzit graph.value(), reps. dokonce
#    # existuje Graph.label() nebo Graph.preferredLabel()
#    result = graph.query(LABEL_QUERY, initBindings={'uri': uri})
#    try:
#        return unicode(next(iter(result))[0])
#    except StopIteration:
#        # no result found
#        if fallback_guess:
#            return uri_to_name(uri)
#        else:
#            return None


#ALL_TERMS_QUERY = prepared_query("""
#    SELECT ?term
#    WHERE {
#        ?term a smartoo:term .
#    }
#""")


# neni potreba: staci pouzit Graph.objecs()
#TYPES_QUERY = prepared_query("""
#    SELECT ?type
#    WHERE {
#        ?term a ?type .
#    }
#""")

# TODO: def discover_types(uri:URIRef)
