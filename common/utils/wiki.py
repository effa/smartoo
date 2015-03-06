from __future__ import unicode_literals

"""
Module of utilities concerning Wikipedia
"""


# NOTE: DEPRECATED -- use knowledge.utils.terms.term_to_name instead
def uri_to_name(uri):
    """
    Transforms URI (of a resource or an article) to the correspoding name.
    """
    return uri.split('/')[-1].replace('_', ' ')


# NOTE: misto name_to_resource_uri pouzivat Term(...)
#def name_to_resource_uri(name):
#    """
#    Transforms a name to URI of the resource (not URL of the article!)
#    """
#    # name normalization
#    name = name[0].upper() + name[1:]
#    name = name.replace(' ', '_')
#    # insert language code and name into general wiki URI format
#    #return 'http://{lang}.wikipedia.org/wiki/{name}'.format(
#    #    lang=language_code,
#    #    name=name)
#    return 'http://dbpedia.org/resource/{name}'.format(name=name)
