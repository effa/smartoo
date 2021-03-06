"""
Module for NLP tasks

# Prabably do a package from this.
"""
from nltk import ParentedTree, word_tokenize, pos_tag


def sentence_to_tree(sentence):
    """
    Given a sentence (as a text), it will transform it to a tree.

    Args:
        sentence: text of a sentence
    Return:
        sentence tree
    """
    assert isinstance(sentence, basestring)

    sentence = pos_tag(word_tokenize(sentence))
    tree = ParentedTree('S', [])
    for token in sentence:
        word, pos = token
        tree.append(ParentedTree(pos, [word]))
    return tree


def is_contextfree(sentence, max_sentence_length=50):
    """
    Returns True if the :sentence: is context-free, False otherwise
    """
    # detect too short or too long sentences
    length = len(sentence.leaves())
    if length < 5 or length > max_sentence_length:
        return False

    # discard questions and exclamation sentences
    if sentence.leaves()[-1] != '.':
        return False

    # discard sentences containing a pronoun, parenthesis or qoatation
    FORBIDDEN_POS_TAGS = {"''", '(', ')', 'PRP', 'PRP$'}
    for node in sentence.subtrees():
        if node.label() in FORBIDDEN_POS_TAGS:
            return False

    FORBIDDEN_WORDS = {':', ';', 'this', 'that', 'these', 'those', 'there', 'then', 'following'}
    for word in sentence.leaves():
        if word.lower() in FORBIDDEN_WORDS:
            return False

    return True


def contextfree_sentences(article, max_sentence_length=50):
    """
    Returns sentences which are likely to be context-free.

    Args:
        article [knowledge.Article]
    Returns:
        list of (context-free) sentences
    """
    contextfree_sentences = []
    for sentence in article.get_sentences():
        if is_contextfree(sentence, max_sentence_length):
            contextfree_sentences.append(sentence)
    return contextfree_sentences


def join_words(words):
    """
    Joins a list of words into single string, removes spaces before punctuation

    Args:
        words: list of words (word can be a string or a token tuple)
    Returns:
        string
    """
    sentence = ''
    last_word = None
    for word in words:
        NOSPACE_AFTER = {'(', '[', '{'}
        NOSPACE_BEFORE = {':', ',', ';', '.', '!', '?', "'", ')', ']', '}',
            'th'}
        # if word is a tuple token, take the first item (= word string)
        if isinstance(word, tuple):
            word = word[0]
        if last_word and last_word not in NOSPACE_AFTER\
                and word not in NOSPACE_BEFORE:
            sentence += ' '
        sentence += word
        last_word = word
    return sentence
