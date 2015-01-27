# TODO: obalit objektem pro persistenci cviceni (a pro paralelni pristup?)
from practice.components import Component


class ExercisesGrader(Component):
    """
    Template for all exercises graders.
    """

    def grade_exercise(self, knowledge_graph):
        """
        Yields exercises.

        Args:
            knowledge_graph (???.KnowledgeGraph): knowledge from which to build
                the exercises
        """
        raise NotImplementedError("interface method not implemented")
