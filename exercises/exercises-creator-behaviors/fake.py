from exercises import ExercisesCreatorBehavior


class Fake(ExercisesCreatorBehavior):
    """
    Fake Exercises Creator Behavior
    --------------------------------

    Returns some exercises, ignorores knowledge graph.
    """

    def create_exercises(self, knowledge_graph):
        # the following is just a construction for an empty generator
        return
        yield
