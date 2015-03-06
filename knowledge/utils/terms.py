"""
Terms related utilities
"""

from __future__ import unicode_literals
from knowledge.namespaces import TERM
from knowledge.utils.termstrie import TermsTrie
from nltk import word_tokenize


def name_to_term(name):
    """
    Returns term created from given name.
    """
    if not name:
        raise ValueError("Invalid argument: " + str(name))

    # name normalization
    name = name.replace(' ', '_')

    return TERM[name]


def term_to_name(term):
    """
    Returns name for the given term.
    """
    name = unicode(term).split('/')[-1].replace('_', ' ')
    return name


def terms_trie_from_term_labels(labels):
    """
    Returns terms trie created from given list of labels
    """
    terms_trie = TermsTrie()
    for label in labels:
        canonical_form = word_tokenize(label)
        terms_trie.add(label, canonical_form)
    return terms_trie
