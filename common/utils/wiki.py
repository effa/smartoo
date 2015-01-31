from __future__ import unicode_literals

"""
Module of utilities concerning Wikipedia
"""


def uri_to_name(uri):
    """
    Transforms URI to the correspoding name (of the article).
    """
    return uri.split('/')[-1].replace('_', ' ')


def name_to_uri(name, language_code='en'):
    """
    Transformas a name to URI.
    """
    # name normalization
    name = name[0].upper() + name[1:]
    name = name.replace(' ', '_')
    # insert language code and name into general wiki URI format
    return 'http://{lang}.wikipedia.org/wiki/{name}'.format(
        lang=language_code,
        name=name)
