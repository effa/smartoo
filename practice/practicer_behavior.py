from abstract_component import ComponentBehavior


class PracticerBehavior(ComponentBehavior):
    """
    Base class for all practicer behaviors.
    """

    def next_exercise(self, exercises, accumulated_feedback):
        """
        Returns new exercise.

        Args:
            exercises: collection of exercises which one will be chosen from
            accumulated_feedback: feedback from previous exercises to help us
                decide which exercise is best for the user
        Returns:
            new exercise
        """
        raise NotImplementedError
