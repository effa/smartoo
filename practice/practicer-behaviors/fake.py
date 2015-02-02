from practice import PracticerBehavior


class Fake(PracticerBehavior):
    """
    Fake practicer behavior
    -----------------------

    Returns an exercises but completely ignores both genereate exercise and
    user's history.
    """
    def next_exercise(self):
        raise NotImplementedError
