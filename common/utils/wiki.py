from __future__ import unicode_literals

"""
Module of utilities concerning Wikipedia
"""


# NOTE: use knowledge.utils.terms.term_to_name instead
def uri_to_name(uri):
    """
    Transforms URI (of a resource or an article) to the correspoding name.
    """
    return uri.split('/')[-1].replace('_', ' ')


def term_to_wiki_uri(term):
    """
    Transforms term (or term name) to URL of corresponding Wikipedia article
    """
    name = unicode(term)
    # name normalization
    name = name[0].upper() + name[1:]
    name = name.replace(' ', '_')
    # insert language code and name into general wiki URI format
    return 'http://en.wikipedia.org/wiki/{name}'.format(name=name)
