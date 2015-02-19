"""
Terms related utilities
"""

from __future__ import unicode_literals
from knowledge.namespaces import TERM


def name_to_term(name):
    """
    Returns term created from given name.
    """
    # name normalization
    name = name.replace(' ', '_')

    return TERM[name]


def term_to_name(term):
    """
    Returns name for the given term.
    """
    name = unicode(term).split('/')[-1].repalce('_', ' ')
    return name
