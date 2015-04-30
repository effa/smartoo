#from exercises.models import Exercise
from practice import PracticerBehavior


class Fake(PracticerBehavior):
    """
    Fake practicer behavior
    -----------------------

    Returns first exercise without using accumulated feedback at all.
    """
    def next_exercise(self, unused_graded_exercises, accumulated_feedback=None,
            feedbacked_exercises=None):
        return unused_graded_exercises[0]
