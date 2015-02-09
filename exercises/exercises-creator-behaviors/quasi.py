from knowledge.utils.sparql import prepared_query, label
from exercises import ExercisesCreatorBehavior
from exercises.models import Exercise
from exercises.utils.distractors import generate_similar_terms
from exercises.utils.distractors import create_choice_list


class Quasi(ExercisesCreatorBehavior):
    """
    Quasi Exercises Creator Behavior
    --------------------------------

    Uses quasi-facts (i.e. facts which encodes a single exercise and are
    useless for anything else).
    """

    def create_exercises(self, knowledge_graph):
        print knowledge_graph
        TERM_IN_SENTENCE_QUERY = prepared_query("""
            SELECT ?before ?term ?after
            WHERE {
                ?quasifact a "term-in-sentence" .
                ?quasifact smartoo:part-before-term ?before .
                ?quasifact smartoo:part-after-term ?after .
                ?quasifact smartoo:term ?term .
            }
        """)

        terms_in_sentence = knowledge_graph.query(TERM_IN_SENTENCE_QUERY)
        print '***'
        for before, term, after in terms_in_sentence:
            correct_answer = label(term, knowledge_graph)
            distractors = generate_similar_terms(term, knowledge_graph)
            choices = create_choice_list(term, distractors, knowledge_graph)
            exercise = Exercise(data={
                'question': '{before} _______ {after}'.format(
                    before=unicode(before),
                    after=unicode(after)),
                'choices': choices,
                'correct-answer': correct_answer
            })
            yield exercise
