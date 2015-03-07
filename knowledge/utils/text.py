"""
Terms related utilities
"""

from __future__ import unicode_literals
#from knowledge.namespaces import TERM
from nltk import ParentedTree, sent_tokenize, word_tokenize, pos_tag
import re


def parse_text(text, terms_trie):
    """
    Given text and a trie of terms, it will parse it, infere terms occurences
    and return list of parsed sentences (each parse sentence consists of
    a tree and list of terms).
    """
    text = preporcess_article_text(text)
    sentences = sent_tokenize(text)
    parsed_sentences = []
    for sentence in sentences:
        sentence = pos_tag(word_tokenize(sentence))
        parsed_sentence = parse_sentence(sentence, terms_trie)
        parsed_sentences.append(parsed_sentence)
    return parsed_sentences


def preporcess_article_text(text):
    """
    Does some preprocessing on the text of a Wikipedia article,
    e.g. removes References, Notes and See also sections.
    """
    BORING_SECTION = re.compile(r"""
        ^\s*
        ==  # section markup
        \s*
        (References | See\ also | External\ links | Notes | Bibliography)
        \s*
        ==
        """, re.VERBOSE)

    text_lines = []

    for line in text.split('\n'):
        if BORING_SECTION.match(line):
            # after first boring section, there is no more usable sentences
            break

        # skip section titles
        if line.startswith('=='):
            continue

        text_lines.append(line)

    return '\n'.join(text_lines)


def parse_sentence(sentence, terms_trie):
    """
    Given (tokenized and tagged) sentence and a trie of terms, it will
    parse it, infere terms occurences and return Trie

    Args:
        sentence: tokenized and tagged sentence
        terms_trie: knowledge.utils.termstrie.TermsTrie
    Return:
        (sentence with inferred terms in form of parse tree,
        list of terms)
    """
    parsed_sentence = ParentedTree('S', [])
    terms = []

    token_index = 0
    while token_index < len(sentence):
        term_label, term_length = _longest_matching_term(sentence,
            token_index, terms_trie)

        if term_length > 0:
            # term found
            term_node = ParentedTree('TERM', [])
            for token in sentence[token_index:token_index + term_length]:
                _append_word_token(term_node, token)
            # TODO: use DBpedia to get more specific type sequence, e.g
            # "TERM:AGENT:PERSON", "TERM:EVENT", "DATE", "NUMBER", ...
            parsed_sentence.append(term_node)
            token_index += term_length
            terms.append(term_label)
        else:
            # there is no term starting from current postion
            token = sentence[token_index]
            _append_word_token(parsed_sentence, token)
            token_index += 1

    return parsed_sentence, terms


def _append_word_token(node, token):
    word, pos_tag = token
    node.append(ParentedTree(pos_tag, [word]))
    #node.append(ParentedTree(pos_tag, [token]))


def _longest_matching_term(text, pos, terms_trie):
    """
    Returns longest matching term and its length from given position

    Returns:
        (unicode, int) or (None, 0) if no term found
    """
    max_length = 0
    current_length = 0
    longest_term = None
    terms_trie.search_start()
    while pos + current_length < len(text):
        token = text[pos + current_length]
        word = token[0]
        if not terms_trie.search_continue(word):
            break
        found_term = terms_trie.search_result()
        if found_term:
            longest_term = found_term
            max_length = current_length + 1
        # go to next token
        current_length += 1
    return (longest_term, max_length)
