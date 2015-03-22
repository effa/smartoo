from __future__ import unicode_literals
from exercises import ExercisesCreatorBehavior
from exercises.models import Exercise


class Fake(ExercisesCreatorBehavior):
    """
    Fake Exercises Creator Behavior
    --------------------------------

    Returns some exercises, ignorores knowledge graph.
    """

    def create_exercises(self, knowledge_graph):
        prepared_exercises = [
            Exercise(data={
                'question': 'When was Henry VIII of England born?',
                'choices': ['1291', '1391', '1491', '1591'],
                'correct-answer': '1491'},
                semantics={'term-pairs': [['Henry VIII', 'Henry VIII']]}
            ),
            Exercise(data={
                'question': 'Who was the successor of Henry VIII of England?',
                'choices': ['Edward VI of England', 'Henry VII of England',
                    'Elizabeht of York', 'Thomas Cromwell'],
                'correct-answer': 'Edward VI of England'
            }),
            Exercise(data={
                'question': 'How many spouses did Henry VII of England have?',
                'choices': ['0', '2', '4', '6'],
                'correct-answer': '6'
            }),
            Exercise(data={
                'question': 'A',
                'choices': ['1', '2', '3', '4'],
                'correct-answer': '1'
            }),
            Exercise(data={
                'question': 'B',
                'choices': ['1', '2', '3', '4'],
                'correct-answer': '1'
            }),
            Exercise(data={
                'question': 'C',
                'choices': ['1', '2', '3', '4'],
                'correct-answer': '1'
            })
        ]
        for exercise in prepared_exercises:
            yield exercise
