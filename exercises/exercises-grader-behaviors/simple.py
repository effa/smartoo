from exercises import ExercisesGraderBehavior
from exercises.models import GradedExercise


class Simple(ExercisesGraderBehavior):
    """
    Simple Exercises Grader Behavior
    ------------------------------

    TODO: description
    """

    def grade_exercise(self, exercise):
        #print type(exercise)
        #print exercise
        return GradedExercise(
            difficulty=0.5,
            correctness=0.5,
            relevance=0.5)
