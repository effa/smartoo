from practice import PracticerBehavior


class PracticerBehavior(PracticerBehavior):
    """
    Fake practicer behavior
    -----------------------

    For testing purposes.
    """
    def start_practice(self):
        raise NotImplementedError

    def next_exercise(self):
        raise NotImplementedError

    def provide_feedback(self, feedback):
        raise NotImplementedError
