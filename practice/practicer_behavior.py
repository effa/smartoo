from abstract_component import ComponentBehavior


class PracticerBehavior(ComponentBehavior):
    """
    Base class for all practicer behaviors.
    """

    def next_exercise(self, graded_exercises, accumulated_feedback):
        """
        Returns new exercise.

        Args:
            graded_exercises: collection of exercises and their grades
            accumulated_feedback: feedback from previous exercises to help us
                decide which exercise is best for the user
        Returns:
            new exercise
        """
        raise NotImplementedError
