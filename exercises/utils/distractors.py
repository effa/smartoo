"""
Module for generating distractors
"""

from knowledge.namespaces import ONTOLOGY, TERM
from random import sample, shuffle

# TODO: inspirace viz procvicinik-v1


# some terms to use if there is not enough of them in the article context
TERMS_OF_TYPE = {
    ONTOLOGY['Person']: [
        TERM['Popeye_the_Sailor_Man'],
        TERM['Asterix'],
        TERM['Meta-Meta-Genie']],
    ONTOLOGY['Event']: [
        TERM['the_Battle_of_Pallet_Town'],
        TERM['race_between_Achilles_and_a_tortoise'],
        TERM['the_Clone_Wars']]
    # TODO ...
}


def generate_similar_terms(term, knowledge_graph, number=3):
    """
    Returns list of terms which are semantically close to the given term.
    Term arse selected fromterms in knowledge graph, but if there is not enough
    of them made-up terms are used (see TERMS_OF_TYPE dictionary).
    """
    # TODO: special treatment for numbers
    all_terms = set(knowledge_graph.all_terms)
    all_terms.discard(term)
    similarity = {t: knowledge_graph.similarity(term, t) for t in all_terms}
    sorted_terms = sorted(similarity, key=similarity.get, reverse=True)
    # NOTE: it's not clear if randomness in selection is usefull at all (or if
    # it has more benefits than negatives), so for now we will simply take
    # :number: most similir terms
    # (if it turns out that randomness is usefull, see _select_similar_terms())
    selected = sorted_terms[:number]

    # if not enough terms have been selected, we will add some made-up terms
    number_rest = number - len(selected)
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


#def _select_similar_terms(terms_similarity, number_max):
#    """
#    Selects :number_max: terms, using some randomness: goes from the most
#    similar term to the least similar and selects each term with the
#    probability based on the similarity and the number of terms needed to
#    select.

#    If there is not enough similar terms, it may return less then :number: terms

#    Args:
#        terms_similarity: dictinary mapping terms to the similarity value
#        number_max: how many terms to select (at most)
#    """
#    sorted_terms = sorted(terms_similarity, key=terms_similarity.get, reverse=True)
#    selected = []
#    for term in sorted_terms:
#        # TODO: take (number_max - len(selected)) into account
#        selection_probability = terms_similarity[term]
#        if random() < selection_probability
#            selected.append(current_term)
#   return selected


def create_choice_list(correct, distractors, knowledge_graph):
    """
    Merges correct answer with distractors, search for labels
    and shuffle/order them.

    Args:
    Returns:
        (list of choices labels, correct answer labels)
    """
    correct_answer_label = knowledge_graph.label(correct)
    choices = [knowledge_graph.label(d) for d in distractors]\
        + [correct_answer_label]
    shuffle(choices)
    # TODO: special treatment for numbers
    return choices, correct_answer_label
