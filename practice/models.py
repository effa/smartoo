#from django.db import models
from practice.


class SessionManager(object):
    """ ...
    """
    def __init__(self, topic):
        self.topic = topic

    def get_new_exercise(self):
        """
        Returns new exercise or None if the practice session is over.
        It can take a while to return a new exercise (they have to be generated
        and graded and this is not instant).

        Returns:
            new exercise (Exercise)
        """
        # demo exercise TODO: trida Exercise, metoda to_dictionary
        exercise = {
            'question': 'When was George Washington born?',
            'options': ['1732', '1782', '1890', '1921']}
        return exercise

    def user_answer(self, answer, feedback):
        """
        Notifies the manager about user answer to the last question.

        Args:
            answer (Char): letter of the answer or None
            feedback (Feedback): user's feedback
        """
        pass
