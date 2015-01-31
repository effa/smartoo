from django.db import models
from common.models import Topic
from components_control import ComponentsSelector
from knowledge.models import KnowledgeBuilder
from exercises.models import ExercisesCreator, ExercisesGrader
from practice.models import Practicer


class Session(models.Model):
    # topic
    topic = models.ForeignKey(Topic)

    # components
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    exercises_creator = models.ForeignKey(ExercisesCreator)
    exercises_grader = models.ForeignKey(ExercisesGrader)
    practicer = models.ForeignKey(Practicer)

    # feedback
    correct_count = models.SmallIntegerField(default=0)
    wrong_count = models.SmallIntegerField(default=0)
    unanswered_count = models.SmallIntegerField(default=0)
    #mean_time = models.IntegerField(null=True, default=None)  # in ms
    invalid_count = models.SmallIntegerField(default=0)
    irrelevant_count = models.SmallIntegerField(default=0)

    # the feedback will be trasform into a single real number (0, 1)
    quality = models.FloatField(null=True, default=None)

    # + details (later) ...

    # time (when created), set automatically on creation
    start = models.DateTimeField(auto_now_add=True)

    # status flag (whether the session was finnished and feedback was used
    # to update performance)
    finnished = models.BooleanField(default=False)

    def select_components(self):
        """
        Selects components for this session.
        """
        selector = ComponentsSelector()
        (self.knowledge_builder, self.exercises_grader, self.exercises_grader,
            self.practicer) = selector.select_components()

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
