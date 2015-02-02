from django.db import models
from components_control import ComponentsSelector
from knowledge.models import Topic, KnowledgeBuilder
from exercises.models import ExercisesCreator, ExercisesGrader
from practice.models import Practicer


class SessionManager(models.Manager):
    def create_with_components(self, topic):
        """
        Creates new session, selects components and saves it to DB.
        """
        session = Session(topic=topic)
        session.select_components()
        session.save()


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

    # manager
    objects = SessionManager()

    def select_components(self):
        """
        Selects components for this session.
        """
        # TODO: vyhodit vhodnou vyjimku, pokud uz jsou vybrany
        selector = ComponentsSelector()
        (self.knowledge_builder, self.exercises_creator, self.exercises_grader,
            self.practicer) = selector.select_components()

    def build_knowledge(self):
        """
        Uses KnowledgeBuilder to build and store knowledge graph.
        """
        pass

    def create_graded_exercises(self):
        """
        Uses ExercisesCreator and ExercisesGrader to create and store exercises
        """
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
                with following items
                TODO: upravit podle smartoo.models.session
                - answered (bool)
                - answer correctly (bool)
                - time to answer in ms (int)
                - invalid question (bool)
        """
        pass
