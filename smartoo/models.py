from django.db import models
from django.db import IntegrityError

from common.settings import SESSION_MAX_LENGTH
from knowledge.fields import TermField
from knowledge.models import KnowledgeGraph, KnowledgeBuilder, Article
from exercises.models import ExercisesCreator, Exercise
from exercises.models import ExercisesGrader, GradedExercise
from practice.models import Practicer
from smartoo import ComponentsSelector
from smartoo.exceptions import SessionError
from wikipedia.exceptions import WikipediaException

import datetime
import logging


logger = logging.getLogger(__name__)

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

    # numbers of correctly answered, wrongly answered and unanswered questions
    correct_count = models.SmallIntegerField(default=0)
    wrong_count = models.SmallIntegerField(default=0)
    unanswered_count = models.SmallIntegerField(default=0)

    #mean_time = models.IntegerField(null=True, default=None)  # in ms

    # numbers of invalid and irrelevant questions
    invalid_count = models.SmallIntegerField(default=0)
    irrelevant_count = models.SmallIntegerField(default=0)

    # final user rating (bad=0, so-so=0.5, good=1)
    final_rating = models.FloatField(default=0.5)

    # how much weight to put on the final rating vs. a single question rating
    FINAL_RATING_WEIGHT = 5.0

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

    def add_final_rating(self, rating):
        """
        Stores final user rating (number between 0 and 1).
        """
        # restrict rating to the interval [0, 1]
        rating = max(0.0, min(1.0, rating))
        self.final_rating = rating
        self.save()

    def get_all_answered_count(self):
        """
        Returns number of all answered questions.
        """
        return self.correct_count + self.wrong_count

    def get_all_questions_count(self):
        """
        Returns number of all questions.
        """
        return self.correct_count + self.wrong_count + self.unanswered_count

    def get_correct_ratio(self):
        """
        Returns ratio of the number of correctly answered questions to
        the number of all answered question. If no questions was answered
        already returns 0.5
        """
        all_count = self.get_all_answered_count()
        if all_count > 0:
            return float(self.correct_count) / all_count
        else:
            return 0.5

    def get_good_questions_count(self):
        """
        Returns number of all questions which were not marked as invalid or
        irrelevant.
        """
        return self.get_all_questions_count()\
            - self.irrelevant_count\
            - self.invalid_count

    def get_performance(self):
        """
        Returns overall performance of the session.
        """
        all_plus = self.get_all_questions_count() + self.FINAL_RATING_WEIGHT
        good_plus = self.get_good_questions_count() + self.FINAL_RATING_WEIGHT * self.final_rating
        performance = float(good_plus) / all_plus
        return performance

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
    # topic and article
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

    # time (when created), set automatically on creation (--> see save())
    #start = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField()

    # status flag (whether the session was finnished and feedback was used
    # to update performance)
    finnished = models.BooleanField(default=False)

    # manager
    objects = SessionManager()

    # override save method
    def save(self, *args, **kwargs):
        # automatically set start field on creation
        if self.id is None:
            self.start = datetime.datetime.now()

        # create article if it wasn't already
        try:
            Article.objects.get_or_create(topic=self.topic)
        except WikipediaException:
            raise ValueError('Invalid topic: {topic}'
                .format(topic=unicode(self.topic)))

        # create feedback if it wasn't already
        if self.feedback_id is None:
            self.feedback = AccumulativeFeedback.objects.create()

        #from django.core import serializers
        #print serializers.serialize('xml', [self], indent=2)

        super(Session, self).save(*args, **kwargs)

    def select_components(self):
        """
        Selects components for this session.
        """
        # TODO: vyhodit vhodnou vyjimku, pokud uz jsou vybrany
        selector = ComponentsSelector(session_manager=Session.objects)
        (self.knowledge_builder, self.exercises_creator, self.exercises_grader,
            self.practicer) = selector.select_components()

    def build_knowledge(self):
        """
        Uses KnowledgeBuilder to build and store knowledge graph for current
        topic.
        """
        try:
            self.knowledge_builder.build_knowledge(self.topic)
        except IntegrityError as exc:
            logger.warning('IntegrityError on knowledge building of ' + unicode(self.topic))
            raise SessionError('Integrity error: ' + exc.message)
        except ValueError as exc:
            logger.warning('ValueError on knowledge building of ' + unicode(self.topic))
            raise SessionError('Value error: ' + exc.message)

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

    def get_unused_graded_exercises(self):
        """
        Returns exercises which were generated but not used already.

        Returns:
            list of graded exercises
        """
        # first find which graded exercises were created for this session
        all_exercises = self.get_graded_exercises()
        # discard exercises which were already used
        # NOTE that used_exercises are not graded ones
        used_exercises = self.get_feedbacked_exercises()
        used_exercises = used_exercises.values_list('exercise', flat=True)
        unused_exercises = all_exercises.exclude(exercise__pk__in=used_exercises)
        return list(unused_exercises)

    def next_exercise(self):
        """
        Returns new exercise or None if the practice session is over.

        Returns:
            new exercise (exercises.models.Exercise) || None
        """
        if self.finnished:
            next_exercise = None
        else:
            feedbacked_exercises = self.get_feedbacked_exercises()
            graded_exercises = self.get_unused_graded_exercises()
            # type of returned object is Exercise, not GradedExercise
            next_exercise = self.practicer.next_exercise(graded_exercises,
                self.feedback, feedbacked_exercises)
            # if there are no more exercises, set the session as finnished
            if not next_exercise:
                self.set_finnished()
        return next_exercise

    def provide_feedback(self, feedback_dictionary):
        """
        Stores feedback for an exercise and accumulates it.

        Args:
            feedback_dictionary: user's feedback as a dictionary
                with following items:
                - "pk" (int) primary key for graded exercise
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
        # TODO: kontrolovat, ze cviceni s timto pk je opravdu z teto session
        exercise = Exercise.objects.get(
            pk=feedback_dictionary["pk"])
        # store the feedback in DB
        feedbacked_exercise = FeedbackedExercise(
            session=self,
            exercise=exercise,
            answered=feedback_dictionary["answered"],
            correct=feedback_dictionary["correct"],
            invalid=feedback_dictionary["invalid"],
            irrelevant=feedback_dictionary["irrelevant"])
        feedbacked_exercise.save()
        # accumulate the feedback
        self.feedback.add(feedbacked_exercise)
        # check if the session is over
        if self.get_questions_count() >= SESSION_MAX_LENGTH:
            self.set_finnished()

    def provide_final_feedback(self, rating):
        self.feedback.add_final_rating(rating)

    def get_questions_count(self):
        return self.feedback.get_all_questions_count()

    def set_finnished(self):
        self.finnished = True
        self.save()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<Session pk={pk}; components=({kb},{ec},{eg},{pr})>'.format(
            pk=self.pk,
            kb=self.knowledge_builder.pk,
            ec=self.exercises_creator.pk,
            eg=self.exercises_grader.pk,
            pr=self.practicer.pk)


class FeedbackedExercise(models.Model):
    """
    Model for storing feedback for one exercise instance (incl. results).
    """
    # identification: session + exercise
    session = models.ForeignKey(Session)
    exercise = models.ForeignKey(Exercise)

    # feedback
    answered = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)
    invalid = models.BooleanField(default=False)
    irrelevant = models.BooleanField(default=False)
    #time (start/end) of the exercise or maybe just time_to_answer?
    #time_to_anser = models.IntegerField(null=True, default=None)  # in ms

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<FeedbackedExercise exercise={exercise}; answered={answered}, correct={correct}, invalid={invalid}, irrelevant={irrelevant}>'.format(
            exercise=unicode(self.exercise),
            answered=self.answered,
            correct=self.correct,
            invalid=self.invalid,
            irrelevant=self.irrelevant)
