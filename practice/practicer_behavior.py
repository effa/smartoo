from abstract_component import ComponentBehavior


class PracticerBehavior(ComponentBehavior):
    """
    Base class for all practicer behaviors.
    """

    def next_exercise(self, unused_graded_exercises, accumulated_feedback,
            feedbacked_exercises, used_graded_exercises):
        """
        Returns new exercise.

        Args:
            unused_graded_exercises: collection of exercises and their grades
                which were not already used
            accumulated_feedback: accumulative feedback from previous exercises
            feedbacked_exercises: collection feedbacked finnished exercises
            used_graded_exercises: collection of graded finnished exercises

        Returns:
            new exercise
        """
        raise NotImplementedError
