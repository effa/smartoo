from django.db import models
from knowledge.models import KnowledgeBuilder


class Session(models.Model):
    # topic
    # ??? topic = models.ForeignKey(Term) ???

    # components
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    # atd ...

    # feedback
    correct_count = models.SmallIntegerField(default=0)
    wrong_count = models.SmallIntegerField(default=0)
    unanswered_count = models.SmallIntegerField(default=0)
    mean_time = models.IntegerField()  # in ms
    invalid_count = models.SmallIntegerField(default=0)
    # + details (later) ...

    # time (when created), set automatically on creation
    start = models.DateTimeField(auto_now_add=True)

    # status flag (whether the session was finnished and feedback was used
    # to update performance)
    finnished = models.BooleanField(default=False)

    def select_components(self):
        # TODO: select components
        pass

    def get_new_exercise(self):
        """
        Returns new exercise or None if the practice session is over.
        It can take a while to return a new exercise (they have to be
        generated and graded and this is not instant).

        Returns:
            new exercise (Exercise)
        """
        # demo exercise TODO: trida Exercise, metoda to_dictionary
        exercise = {
            'question': 'When was George Washington born?',
            'options': ['1732', '1782', '1890', '1921']}
        return exercise

    def provide_feedback(self, feedback):
        """
        Notifies the manager about user answer to the last question.

        Args:
            feedback: user's feedback, JSON string representing dictionary
                with following items:
                - answered (bool)
                - answer correctly (bool)
                - time to answer in ms (int)
                - invalid question (bool)
                - (TODO later: details about invalidity)
        """
        pass
