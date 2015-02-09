"""
Utilities for SPARQL language
"""

from __future__ import unicode_literals
from rdflib.plugins.sparql import prepareQuery
from common.utils.wiki import uri_to_name
from knowledge.namespaces import NAMESPACES_DICT


def prepared_query(query_string):
    """
    Returns prepared query with initialized standard namespaces bindings.
    """
    return prepareQuery(query_string, initNs=NAMESPACES_DICT)

# ---------------------------------------------------------------------------
#  preprepared queries
# ---------------------------------------------------------------------------

LABEL_QUERY = prepared_query("""
    SELECT ?label
    WHERE {
        ?uri rdfs:label ?label
    }
""")


def label(uri, graph, fallback_guess=True):
    """
    Returns label for given uri reference stated in the given graph.

    Args:
        uri: URI reference to the object for which to find label
        graph: where to search for the label
        fallback_guess: guess the label (using URI) if label wasn't found
    Returns:
        label [unicode]
    """
    result = graph.query(LABEL_QUERY, initBindings={'uri': uri})
    try:
        return unicode(next(iter(result))[0])
    except StopIteration:
        # no result found
        if fallback_guess:
            return uri_to_name(uri)
        else:
            return None


ALL_TERMS_QUERY = prepared_query("""
    SELECT ?term
    WHERE {
        ?term a smartoo:term .
    }
""")


#TYPES_QUERY = prepared_query("""
#    TODO
#""")

# TODO: def discover_types(uri:URIRef)
