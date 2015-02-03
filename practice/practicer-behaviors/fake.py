from exercises.models import Exercise
from practice import PracticerBehavior


class Fake(PracticerBehavior):
    """
    Fake practicer behavior
    -----------------------

    Returns an exercises but completely ignores both genereated exercises and
    user's accumulated feedback.
    """
    def next_exercise(self, exercises, accumulated_feedback):
        return Exercise(data={
            'question': 'When was Henry VIII of England born?',
            'options': ['1291', '1391', '1491', '1591'],
            'correct-answer': '1491'
        })
