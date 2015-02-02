from exercises import ExercisesGraderBehavior


class Fake(ExercisesGraderBehavior):
    """
    Fake Exercises Grader Behavior
    ------------------------------

    Just gives some grades without looking at the exercises.
    """

    def grade_exercise(self, exercise):
        pass
