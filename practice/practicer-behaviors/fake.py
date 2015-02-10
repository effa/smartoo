#from exercises.models import Exercise
from practice import PracticerBehavior


class Fake(PracticerBehavior):
    """
    Fake practicer behavior
    -----------------------

    Returns first exercise without using accumulated feedback at all.
    """
    def next_exercise(self, graded_exercises, accumulated_feedback):
        return graded_exercises[0]
