from abstract_component import ComponentBehavior


class PracticerBehavior(ComponentBehavior):
    """
    Base class for all practicer behaviors.
    """
    #def start_practice(self):
    #    """
    #    Start new practice session.
    #    """
    #    raise NotImplementedError

    def next_exercise(self):
        """
        Returns new exercise.
        """
        raise NotImplementedError

    #def provide_feedback(self, feedback):
    #    """
    #    Provide feedback after an exercise.
    #    """
    #    raise NotImplementedError
