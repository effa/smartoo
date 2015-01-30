from abstract_component import ComponentBehavior


class ExercisesGraderBehavior(Component):
    """
    Template for all exercises grader behaviors.
    """

    def grade_exercise(self, knowledge_graph):
        """
        Yields exercises.

        Args:
            knowledge_graph (???.KnowledgeGraph): knowledge from which to build
                the exercises
        """
        raise NotImplementedError("interface method not implemented")
