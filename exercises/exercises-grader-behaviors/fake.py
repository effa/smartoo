from exercises import ExercisesGraderBehavior
from exercises.models import ExerciseGrades


class Fake(ExercisesGraderBehavior):
    """
    Fake Exercises Grader Behavior
    ------------------------------

    Just gives some grades without looking at the exercises.
    """

    def grade_exercise(self, exercise):
        return ExerciseGrades(
            difficulty=0.5,
            correctness=0.5,
            relevance=0.5)
