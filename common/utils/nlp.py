"""
Module for NLP tasks

# Prabably do a package from this.
"""


def contextfree_sentences(article):
    """
    Returns sentences which are likely to be context-free.

    Args:
        article [knowledge.Article]
    Returns:
        list of (context-free) sentences
    """
    # TODO: some simple heuristic for that, later some sophisticated
    # anafora resolution would be great
    return article.get_sentences()


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
