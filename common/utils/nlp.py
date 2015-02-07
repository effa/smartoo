"""
Module for NLP tasks

# Prabably do a package from this.
"""


def contextfree_sentences(article):
    """
    Returns sentences which are likely to be context-free.

    Args:
        article [knowledge.Article]
    """
    # TODO: some simple heuristic for that, later some sophisticated
    # anafora resolution would be great
    pass


class Text(object):
    """
    Neni uplne jasne, ale bude potreba trida na posloupnost tokenu a struktur
    a praci s nimi, ktera odstini od samotne implementace.
    """
    pass
    # TODO: napred se dobre naucit NLTK a vyuzivat ji, at nemusim vynalezat
    # kolo

    def plain_text(self):
        """
        Remove all tags and structures and join tokens into text (single
        string).
        """
        pass
