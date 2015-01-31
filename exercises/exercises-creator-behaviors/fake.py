from exercises import ExercisesCreatorBehavior


class ExercisesCreatorBehavior(ExercisesCreatorBehavior):
    """
    Fake Exercises Creator Behavior
    --------------------------------

    Pretends to creates exercises. For testing purposes only.
    """

    def create_exercises(self, knowledge_graph):
        # the following is just a construction for an empty generator
        return
        yield
