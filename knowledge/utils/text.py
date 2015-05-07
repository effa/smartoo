# encoding=utf-8

"""
Terms related utilities
"""

from __future__ import unicode_literals

from knowledge.utils.terms import name_to_term

from collections import defaultdict
from nltk import ParentedTree, sent_tokenize, word_tokenize, pos_tag
import re


def shallow_parsing(text):
    """
    Tokenizes text to words and sentences and assings a tag to each word.
    """
    text = preporcess_article_text(text)
    sentences = sent_tokenize(text)
    parsed_sentences = []
    for sentence in sentences:
        parsed_sentence = pos_tag(word_tokenize(sentence))
        parsed_sentences.append(parsed_sentence)
    return parsed_sentences


def shallow_parsing_phrases(phrases):
    """
    Tokenizes and tags phrases.
    """
    return [pos_tag(word_tokenize(phrase)) for phrase in phrases]


def preporcess_article_text(text):
    """
    Does some preprocessing on the text of a Wikipedia article,
    e.g. removes References, Notes and See also sections.
    """
    BORING_SECTION = re.compile(r"""
        ^\s*
        =+  # section markup
        \s*
        §?  # there might be this paragraph sign
        (References | See\ also | External\ links | Notes | Bibliography)
        \s*
        =+
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


def terms_inference(sentences, terms_trie):
    """
    Given (tokenized and tagged) sentences and a trie of terms, it will
    infere terms occurences and return list of sentence trees.

    Args:
        sentences: shallow-parsed text
        terms_trie: trie of terms
    Return:
        list of shallow parse trees with inferred terms,
        dictionary of refferences to terms positions
    """
    parsed_sentences = []
    terms_positions = defaultdict(list)
    for sentence in sentences:
        parsed_sentence = ParentedTree('S', [])

        token_index = 0
        while token_index < len(sentence):
            term_label, term_length = _longest_matching_term(sentence,
                token_index, terms_trie)

            if term_length > 0:
                # term found
                term_node = ParentedTree('TERM', [])

                term = name_to_term(term_label)
                term_node.term = term
                terms_positions[term].append(term_node)

                for token in sentence[token_index:token_index + term_length]:
                    _append_word_token(term_node, token)
                parsed_sentence.append(term_node)

                token_index += term_length

            else:
                # there is no term starting from current postion
                token = sentence[token_index]
                _append_word_token(parsed_sentence, token)
                token_index += 1

        parsed_sentences.append(parsed_sentence)

    return parsed_sentences, terms_positions


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
