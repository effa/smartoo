"""
Module for logistic model of a student
"""

from math import exp  # , sqrt, log


def correct_answer_probability(knowledge, difficulty, slope=1, choices_count=4):
    """
    Returns probability of corrcet answer in 3PL model,
    i.e. P(knowledge, a=slope, b=difficulty, c=(1/choices_count)).
    """
    guess = 1.0 / choices_count
    probability = guess + (1 - guess) / (1 + exp(slope * (difficulty - knowledge)))
    return probability


def practice_likelihood(correct, incorrect, knowledge):
    """
    Computes likelihood of a practice (given by lists of exercise difficulties,
    which were answered correctly and incorrectly) for a given knowledge level.
    """
    probability = 1
    for difficulty in correct:
        probability *= correct_answer_probability(knowledge, difficulty)
    for difficulty in incorrect:
        probability *= (1 - correct_answer_probability(knowledge, difficulty))
    return probability


def estimate_knowledge(correct, incorrect):
    """
    Returns the knowledge which maximizes the practice likelihood.
    """
    # which knowledges to consider
    FROM, STEP, TO = -1.0, 0.05, 2.0

    # default knowledge is 0, as we use normalized exercises difficulties
    DEFAULT_KNOWLEDGE = 0

    # maximum likelihood estimation of knowledge
    knowledge, probability = 0, 0
    k = FROM
    while k <= TO:
        p = practice_likelihood(correct, incorrect, k)
        if p > probability:
            knowledge, probability = k, p
        k += STEP

    # make the estimates more stable at the beginning
    n = len(correct) + len(incorrect)
    stabilizator = 1.0 / (0.25 * (n ** 2) + 1)
    knowledge = stabilizator * DEFAULT_KNOWLEDGE + (1 - stabilizator) * knowledge
    return knowledge
