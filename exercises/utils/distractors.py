"""
Module for generating distractors
"""

from knowledge.namespaces import ONTOLOGY, TERM
from random import sample, shuffle, random


# some terms to use if there is not enough of them in the article context
TERMS_OF_TYPE = {
    ONTOLOGY['Agent']: [
        TERM['Popeye_the_Sailor_Man'],
        TERM['Asterix'],
        TERM['Meta-Meta-Genie']],
    ONTOLOGY['Event']: [
        TERM['the_Battle_of_Pallet_Town'],
        TERM['race_between_Achilles_and_a_tortoise'],
        TERM['the_Clone_Wars']],
    ONTOLOGY['Place']: [
        TERM['Pallet_Town'],
        TERM['Tumbolia'],
        TERM['Statue_of_Achilles_in_Hyde_Park']],
    ONTOLOGY['Species']: [
        TERM['Pikachu'],
        TERM['Goldfish'],
        TERM['Penguin_with_glasses']]
}


def generate_similar_terms(term, knowledge_graph, number=3):
    """
    Returns list of terms which are semantically close to the given term.
    Term arse selected fromterms in knowledge graph, but if there is not enough
    of them made-up terms are used (see TERMS_OF_TYPE dictionary).
    """
    all_terms = set(knowledge_graph.all_terms)
    all_terms.discard(term)
    similarity = {t: knowledge_graph.similarity(term, t) for t in all_terms}
    sorted_terms = sorted(similarity, key=similarity.get, reverse=True)
    selected = sorted_terms[:number]

    selected = []
    i = 0
    number_rest = number
    while number_rest > 0:
        if i >= len(sorted_terms):
            break
        if random() <= selection_probability(sorted_terms, similarity, i, number_rest):
            number_rest -= 1
            selected.append(sorted_terms[i])
        i += 1

    # if not enough terms have been selected, we will add some made-up terms
    #number_rest = number - len(selected)
    if number_rest > 0:
        types = knowledge_graph.types(term)
        # at first try to find terms of the same type
        for term_type in TERMS_OF_TYPE:
            if term_type in types:
                selected += TERMS_OF_TYPE[term_type][:number_rest]
                number_rest = number - len(selected)
                if number_rest == 0:
                    break
        # if the term was not in any category and there are still some terms
        # missing, take random make-up terms
        if number_rest > 0:
            all_terms = {t for l in TERMS_OF_TYPE.values() for t in l}
            # removes the terms which were alread selected to prevent duplicats
            all_terms.difference_update(selected)
            # if there is not enough made up terms, take all of them
            if len(all_terms) <= number_rest:
                selected += all_terms
            else:
                # randomly select rest terms
                selected += sample(all_terms, number_rest)

    return selected


def selection_probability(terms, similarities, i, k=1):
    #urgency = float(k) / (k + 1)
    # make sure the current similarity is not too close to 0
    similarity_now = max(0.1, similarities[terms[i]])
    if i + k < len(similarities):
        similarity_next = similarities[terms[i + k]]
    else:
        similarity_next = 0.0
    relative_similarity_difference = (similarity_now - similarity_next) / similarity_now
    selection_probability = 0.5 + 0.5 * relative_similarity_difference
    return selection_probability


def create_choice_list(choices, knowledge_graph):
    """
    Search for labels of choices and shuffle/order them.

    Args:
        choices: list of terms
        knowledge_graph: context (knowledge.models.KnowledgeGraph)
    Returns:
        (list of choices labels, correct answer labels)
    """
    choices = [knowledge_graph.label(c) for c in choices]
    shuffle(choices)
    return choices
