from abstract_component import ComponentBehavior


class ExercisesGraderBehavior(ComponentBehavior):
    """
    Base class for all exercises grader behaviors.
    """
    def grade_exercise(self, exercise):
        """
        Estimates exerice parameters such as correctness and difficulty.

        Args:
            exercise (exercises.models.Exercise): exercise to grade
        Returns:
            grades (exercises.models.Grades)
        """
        raise NotImplementedError("interface method not implemented")
