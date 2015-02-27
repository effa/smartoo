from __future__ import unicode_literals
from django.db import models
from abstract_component.models import Component
from common.fields import DictField
from knowledge.models import KnowledgeGraph


# ---------------------------------------------------------------------------
#  Components
# ---------------------------------------------------------------------------

class ExercisesCreator(Component):
    """
    Model for exercises creator component.
    """

    BEHAVIORS_PATH = 'exercises/exercises-creator-behaviors/'

    @classmethod
    def get_behaviors_path(cls):
        return cls.BEHAVIORS_PATH

    def create_exercises(self, knowledge_graph, yielding=True):
        """
        Creates, stores and yeilds exercises.

        Args:
            knowledge_graph (knowledge.models.KnowledgeGraph)
        Yields:
            exercises (exercises.models.Exercise)
        """
        # first check whether the exercises are not already built (TODO: tohle
        # je potreba zjistovat pres specialni tabulku, jinak muzou nastat
        # problemy)
        exercises = Exercise.objects.filter(
            knowledge_graph=knowledge_graph,
            exercises_creator=self)
        if exercises:
            if yielding:
                for exercise in exercises:
                    yield exercise
            return

        behavior = self.get_behavior()
        for exercise in behavior.create_exercises(knowledge_graph):
            exercise.exercises_creator = self
            exercise.knowledge_graph = knowledge_graph
            exercise.save()
            if yielding:
                yield exercise

    def __unicode__(self):
        return '<ExercisesCreator {name}; parameters={parameters}>'.format(
            name=self.behavior_name,
            parameters=self.parameters)


class ExercisesGrader(Component):
    """
    Model for exercises grader component.
    """

    BEHAVIORS_PATH = 'exercises/exercises-grader-behaviors/'

    @classmethod
    def get_behaviors_path(cls):
        return cls.BEHAVIORS_PATH

    def create_graded_exercises(self, knowledge_graph, exercises_creator):
        """
        Creates exercises using provided :exercises_creator: and grades them
        immediatelly as they are yielded. Exercises and grades are stored in
        DB, nothing is returned.

        Args:
            knowledge_graph (knowledge.models.KnowledgeGraph): knowledge graph
                from which to build the exercises
            exercises_creator (exercises.models.ExercisesCreator): component to
                use for exercises yielding
        Raises:
            IntegrityError: if knowledge_graph or exercise_creator is not
                already stored in DB (we need their primary keys)
        """
        for exercise in exercises_creator.create_exercises(knowledge_graph):
            # compute grades and store them in DB
            self.grade_exercise(exercise)

    def grade_exercise(self, exercise):
        """
        Computes grade and stores them (doesn't return anything).

        Args:
            exercise (exercises.model.Exercise): exercise to grade, has to be
                already stored in DB
        Raises:
            IntegrityError: if the exercise is not already stored in DB
        """
        # first check whether the exercises are not already built (TODO: tohle
        # je potreba zjistovat pres specialni tabulku, jinak muzou nastat
        # problemy)
        if GradedExercise.objects.filter(
                exercise=exercise,
                exercises_grader=self).exists():
            return  # nothing to do

        behavior = self.get_behavior()
        grades = behavior.grade_exercise(exercise)
        grades.exercise = exercise
        grades.exercises_grader = self
        grades.save()

    def __unicode__(self):
        return '<ExercisesGrader {name}; parameters={parameters}>'.format(
            name=self.behavior_name,
            parameters=self.parameters)


# ---------------------------------------------------------------------------
#  Exercise related models
# ---------------------------------------------------------------------------

class Exercise(models.Model):
    """
    Model for all exercises.
    """
    # metadata (about origin)
    knowledge_graph = models.ForeignKey(KnowledgeGraph)
    exercises_creator = models.ForeignKey(ExercisesCreator)

    # exercise data and behavior
    # NOTE: For now, all questions are uniform (multiplechoice), but later, we
    # will want to have many types of exercises. Than we will need another
    # model for ExercisesType to store information about exercise structure
    # (schema), HTML partial template and JS for grabbing user answer from this
    # HTML partial. In this model we will just add a line to specify a foreign
    # key for ExerciseType.
    # For now, the data is a simple dictionary containing the following
    # fields: "question", "choices" and "correct-answer".
    data = DictField(default=dict)

    # NOTE: To make things simplier, I will leave the exercise itself
    # completely semantitc-free and provide semantic metadata separatedly, so
    # that the graders have some data to use for grading.
    # TODO: specify the semantic metadata

    def __unicode__(self):
        return '<Exercise {data}>'.format(data=self.data)


class GradedExercise(models.Model):
    # identification: which exercise + which grader
    exercise = models.ForeignKey(Exercise)
    exercises_grader = models.ForeignKey(ExercisesGrader)

    # difficulty: probability that a user doesn't know the correct answer
    difficulty = models.FloatField()

    # probability that the question is correct syntactically, semantically, ...
    correctness = models.FloatField()

    # relevance: probability of the question being relevant to the topic
    relevance = models.FloatField()

    def __unicode__(self):
        return ('<GradedExercise exercise=%s difficulty=%s, correctness=%s,'
            + ' relevance=%s>') % (self.exercise, self.difficulty,
                    self.correctness, self.relevance)
