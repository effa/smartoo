"""
Module for generating distractors
"""

from random import shuffle
from knowledge.utils.sparql import label

# TODO: inspirace viz procvicinik-v1


def generate_similar_terms(term, knowledge_graph, number=3):
    all_terms = knowledge_graph.get_all_terms()
    all_terms.discard(term)
    if len(all_terms) <= number:
        # TODO: vygenerovat smyslene pojmy (vtipne, napr. z formalu)
        return list(all_terms)
    else:
        # TODO: randomly pick :number: terms
        pass


def create_choice_list(correct, distractors, knowledge_graph):
    """
    Merges correct answer with distractors, search for label
    and shuffle/order them.
    """
    choices = distractors + [correct]
    choices = [label(choice, knowledge_graph) for choice in choices]
    shuffle(choices)
    # TODO: special treatment for numbers
    return choices
