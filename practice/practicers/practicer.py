# TODO: obalit objektem pro persistenci cviceni (a pro paralelni pristup?)
from practice.components import Component


class Practicer(Component):
    """
    Template for all practicers.
    """
    def start_practice(self):
        """
        Start new practice session.
        """
        raise NotImplementedError("interface method not implemented")

    def next_exercise(self):
        """
        Returns new exercise.
        """
        raise NotImplementedError("interface method not implemented")

    def provide_feedback(self, feedback):
        """
        Provide feedback after an exercise.
        """
        raise NotImplementedError("interface method not implemented")
