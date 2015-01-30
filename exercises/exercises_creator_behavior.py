from abstract_component import ComponentBehavior


class ExercisesCreatorBehavior(ComponentBehavior):
    """
    Interface (template) for all exercises creator behaviors.
    """

    def create_exercises(self, knowledge_graph):
        """
        Yields exercises.

        Args:
            knowledge_graph (???.KnowledgeGraph): knowledge from which to build
                the exercises
        """
        raise NotImplementedError("interface method not implemented")
