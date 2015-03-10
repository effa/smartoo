from math import sqrt


# ----------------------------------------------------------------------------
# Information retreival metrics and scoring functions
# ----------------------------------------------------------------------------

def euclidian_length(document):
    """
    Given a document (dictionary: token -> number of occurrences), computes
    its euclidian length.
    """
    length = 0
    for count in document.values():
        if isinstance(count, list):
            count = len(count)
        length += count * count
    length = sqrt(length)
    return length


def cosine_similarity(document1, document2):
    """
    Computes cosine similarity between two documents. If one document is
    query (i.e. significantly shorter), put it as :document1:

    Args:
        document1: dictionary (token -> number of occurences)
        document2: dictionary (token -> number of occurences)
        Implementation note: put the shorter document as :document1:
    Returns:
        cosine similarity measure [float]
    """
    # compute dot product (document1 . document2)
    dot_product = 0
    for token in document1:
        dot_product += document1[token] * document2.get(token, 0)

    # compute euclidian lengths of documents
    document1_length = euclidian_length(document1)
    document2_length = euclidian_length(document2)

    if document1_length > 0 and document2_length > 0:
        # normalize dot product
        return dot_product / (document1_length * document2_length)
    else:
        return 0.0


def cosine_similarity_exercise_article(exercise, article):
    """
    Modified version of cosine_similarity() function to more convenient
    and efficient computation when the documents are exercise (terms in
    an exercise) and an article.
    """
    # compute dot product (exercise . article)
    dot_product = 0
    for term, exercise_count in exercise.items():
        dot_product += exercise_count * len(article.get_term_positions(term))

    # compute euclidian lengths of documents
    exercise_length = euclidian_length(exercise)
    article_length = article.euclidian_length

    if exercise_length > 0 and article_length > 0:
        # normalize dot product
        return dot_product / (exercise_length * article_length)
    else:
        return 0.0
