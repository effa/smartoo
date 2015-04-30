"""
Utilities for computing exercise difficulty
"""


def difficulty_normalization(difficulty, from_interval=(0, 1), to_interval=(-2, 2)):
    """
    Maps given 'difficulty' from 'from_interval' to 'to_interval'.
    Normalized difficulty is necessary for use in the logistic model.
    """
    size_ratio = float(to_interval[1] - to_interval[0])\
        / (from_interval[1] - from_interval[0])
    normalized_difficulty = (difficulty - from_interval[0]) * size_ratio\
        + to_interval[0]
    return normalized_difficulty


def normalized_average_similarity(similarities):
    """
    Computes average similarity and normalizes it for use in logistic model
    """
    average_similarity = sum(similarities) / len(similarities)
    difficulty = difficulty_normalization(average_similarity)
    return difficulty
