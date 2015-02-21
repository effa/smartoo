from django.db import models
from django.db import IntegrityError
from knowledge.fields import TermField
from knowledge.models import KnowledgeGraph, KnowledgeBuilder
from exercises.models import ExercisesCreator, GradedExercise, ExercisesGrader
from practice.models import Practicer
from smartoo import ComponentsSelector
from smartoo.exceptions import SessionError


#class AccumulativeFeedbackManager(models.Manager):
#    def create_empty_feedback(self):
#        """
#        Creates empty accumulative feedback and stores it to DB.

#        Returns:
#            empty accumulative feedback (smartoo.models.AccumulativeFeedback)
#        """
#        pass
#        #feedback = AccumulativeFeedback()
#        #feedback.save()
#        #return feedback


class AccumulativeFeedback(models.Model):
    """
    Model for storing feedback for the whole session.
    """
    correct_count = models.SmallIntegerField(default=0)
    wrong_count = models.SmallIntegerField(default=0)
    unanswered_count = models.SmallIntegerField(default=0)
    #mean_time = models.IntegerField(null=True, default=None)  # in ms
    invalid_count = models.SmallIntegerField(default=0)
    irrelevant_count = models.SmallIntegerField(default=0)
    # TODO: user_grade: uzivatelske hodnoceni na zaver, neco ve stylu Desny,
    # Prumer, OK (mozna jako realne cislo - kliknuti na osu)

    # the feedback will be trasform into a single real number (0, 1)
    # TODO: get_quality: pokud jeste nebylo nastaveno, tak se spocita a ulozi
    # (po zacatek by stacilo to pokazde pocitat znova)
    #quality = models.FloatField(null=True, default=None)

    # + details (later) ...

    # manager:
    #objects = AccumulativeFeedbackManager()

    def add(self, feedback):
        """
        Accumulate new feedback.

        Args:
            feedback (smartoo.models.FeedbackExercise): new feedback
        """
        if feedback.answered:
            if feedback.correct:
                self.correct_count += 1
            else:
                self.wrong_count += 1
        else:
            self.unanswered_count += 1
        self.invalid_count += int(feedback.invalid)
        self.irrelevant_count += int(feedback.irrelevant)
        # TODO: quality calculation ?
        # store the updated accumulative feedback to DB
        self.save()


# NOTE: Due to migrations serializations issues (and Python 2), this method for
# creating empty feedback has to be in the main body of the module. It can't be
# method (neither in manager nor in the model as as static class).
# Using default=AccumuliveFeedback.objects.save also doesn't work.
# NOTE: Strange SessionManager works without these problems....
#def create_empty_feedback():
#    """
#    Creates empty accumulative feedback and stores it to DB.

#    Returns:
#        empty accumulative feedback
#    """
#    #return AccumulativeFeedback.objects.create()
#    feedback = AccumulativeFeedback()
#    #feedback.save()
#    return feedback


class SessionManager(models.Manager):
    def create_with_components(self, topic):
        """
        Creates new session, selects components and saves it to DB.

        Args:
            topic: identifies topic for this session
        Retruns:
            created session (smartoo.models.Sesion)
        """
        session = Session(topic=topic)
        session.select_components()
        session.save()
        return session


class Session(models.Model):
    """
    Model for one practice session.
    """
    # topic
    topic = TermField()

    # components
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    exercises_creator = models.ForeignKey(ExercisesCreator)
    exercises_grader = models.ForeignKey(ExercisesGrader)
    practicer = models.ForeignKey(Practicer)

    # feedback
    # NOTE: default=AccumulativeFeedback.objects.create doesn't work because of
    # some migrations serialization issues.
    # Workarround: I will save feedback on saving session
    feedback = models.OneToOneField(AccumulativeFeedback)

    # time (when created), set automatically on creation
    start = models.DateTimeField(auto_now_add=True)

    # status flag (whether the session was finnished and feedback was used
    # to update performance)
    finnished = models.BooleanField(default=False)

    # manager
    objects = SessionManager()

    # override save method
    def save(self, *args, **kwargs):
        # create feedback if it wasn't already
        if self.feedback_id is None:
            self.feedback = AccumulativeFeedback.objects.create()
        super(Session, self).save(*args, **kwargs)

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
        Uses KnowledgeBuilder to build and store knowledge graph for current
        topic.
        """
        try:
            self.knowledge_builder.build_knowledge(self.topic)
        except (IntegrityError, ValueError):
            # TODO: zrava + retezeni? + logovani
            raise SessionError

    def get_knowledge_graph(self):
        """
        Returns knowledge graph created for this session.

        Raises:
            ObjectDoesNotExist: if knowledge graph hasn't been already created
        Returns:
            knowledge graph
        """
        knowledge_graph = KnowledgeGraph.objects.get(
            topic=self.topic,
            knowledge_builder=self.knowledge_builder)
        return knowledge_graph

    def create_graded_exercises(self):
        """
        Uses ExercisesCreator and ExercisesGrader to create and store exercises
        """
        # retrieve knowledge graph for the session topic and used knowledge
        # builder
        # TODO (?) nejprve kontrolovat zda uz nejsou cviceni vytvorena?
        knowledge_graph = self.get_knowledge_graph()
        self.exercises_grader.create_graded_exercises(
            knowledge_graph=knowledge_graph,
            exercises_creator=self.exercises_creator)

    def get_graded_exercises(self):
        """
        Returns all graded exercises for this session.
        """
        return GradedExercise.objects.filter(
            exercise__knowledge_graph=self.get_knowledge_graph(),
            exercise__exercises_creator=self.exercises_creator,
            exercises_grader=self.exercises_grader)

    def get_feedbacked_exercises(self):
        """
        Returns exercises which were (already) used in this session (together
        with provided feedback).
        """
        return FeedbackedExercise.objects.filter(session=self)

    def get_unused_exercises(self):
        """
        Returns exercises which were generated but not used already.

        Returns:
            list of exercises
        """
        # first find which graded exercises were created for this session
        all_exercises = self.get_graded_exercises()
        # discard exercises which were already used
        used_exercises = self.get_feedbacked_exercises()\
            .values_list('graded_exercise', flat=True)
        unused_exercises = all_exercises.exclude(pk__in=used_exercises)
        return list(unused_exercises)

    def next_exercise(self):
        """
        Returns new exercise or None if the practice session is over.

        Returns:
            new exercise (exercises.models.GradedExercise) || None
        """
        graded_exercises = self.get_unused_exercises()
        graded_exercise = self.practicer.next_exercise(graded_exercises,
            self.feedback)
        # return graded exercise (not only exercise) so that primary key of
        # the graded exercise can be saved into request.sesion
        return graded_exercise

    def provide_feedback(self, feedback_dictionary):
        """
        Stores feedback for an exercise and accumulates it.

        Args:
            feedback_dictionary: user's feedback as a dictionary
                with following items:
                - "exercise-pk" (int) primary key for graded exercise
                - "answered" (bool)
                - "correct" (bool)
                - "invalid" (bool)
                - "irrelevant" (bool)
                (? "answer" ?)
                (later add more details such as time to answer in ms)
                (see exercises.models.FeedbackedExercise)

        Note: Before calling this method, session instance should be already
        saved (because feedback is created on saving the session)...
        originally I did this because of migration serialization issues,
        but it's actully good not to have feedback which doesn't belong to
        any stored session.
        """
        # get the exercise from DB
        graded_exercise = GradedExercise.objects.get(
            pk=feedback_dictionary["exercise-pk"])
        # store  the feedback in DB
        feedbacked_exercise = FeedbackedExercise(
            session=self,
            graded_exercise=graded_exercise,
            answered=feedback_dictionary["answered"],
            correct=feedback_dictionary["correct"],
            invalid=feedback_dictionary["invalid"],
            irrelevant=feedback_dictionary["irrelevant"])
        feedbacked_exercise.save()
        # accumulate the feedback
        self.feedback.add(feedbacked_exercise)


class FeedbackedExercise(models.Model):
    """
    Model for storing feedback for one exercise instance (incl. results).
    """
    # identification: session + exercise
    session = models.ForeignKey(Session)
    graded_exercise = models.ForeignKey(GradedExercise)

    # feedback
    answered = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)
    invalid = models.BooleanField(default=False)
    irrelevant = models.BooleanField(default=False)
    #time (start/end) of the exercise or maybe just time_to_answer?
    #time_to_anser = models.IntegerField(null=True, default=None)  # in ms
