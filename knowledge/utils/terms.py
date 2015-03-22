"""
Terms related utilities
"""

from __future__ import unicode_literals
from knowledge.namespaces import TERM, ONTOLOGY
from knowledge.utils.termstrie import TermsTrie


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


#def terms_trie_from_term_labels(labels):
    #"""
    #Returns terms trie created from given list of labels
    #"""
    #terms_trie = TermsTrie()
    #for label in labels:
    #    terms_trie.add_with_subnames(label)
    #return terms_trie


def bulk_create_terms_trie(terms, knowledge_graph=None):
    """
    Returns terms trie created from given list of labels

    Args:
        terms: list of tuples of term label and shallowed parsed term
    Retruns:
        terms trie
    """
    terms_trie = TermsTrie()
    for name, tagged_name in terms:
        if knowledge_graph and ONTOLOGY['Person'] in knowledge_graph.types(name_to_term(name)):
            terms_trie.add_with_subnames(name, tagged_name)
        else:
            terms_trie.add(name, tagged_name)
    return terms_trie


def create_term_pairs_1toN(leading_term, other_terms):
    """
    Creates list of term *names* of :leading_term: with each of :other_terms:
    """
    pairs = []
    for other_term in other_terms:
        pairs.append((term_to_name(leading_term), term_to_name(other_term)))
    return pairs
