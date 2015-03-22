from abstract_component import ComponentBehavior


class ExercisesCreatorBehavior(ComponentBehavior):
    """
    Base class for all exercises creator behaviors.
    """
    def create_exercises(self, knowledge_graph):
        """
        Yields exercises.

        Args:
            knowledge_graph (knowledge.models.KnowledgeGraph)
        Yields:
            exercises (exercises.models.Exercise)
        """
        raise NotImplementedError("interface method not implemented")
