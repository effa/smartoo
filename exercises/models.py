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

    BEHAVIORS_PATH = 'exercises/exercises-grader-behaviors'

    @classmethod
    def get_behaviors_path(cls):
        return cls.BEHAVIORS_PATH

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
    # TODO: specify the semanitc metadata

    def __unicode__(self):
        return '<Exercise {data}>'.format(data=self.data)


class ExerciseGrades(models.Model):
    exercise = models.ForeignKey(Exercise)
    #exercise_grader = models.ForeignKey(ExerciseGrader)

    # difficulty: probability that a user doesn't know the correct answer
    difficulty = models.FloatField()

    # probability that the question is correct syntactically, semantically, ...
    correctness = models.FloatField()

    # relevance: probability of the question being relevant to the topic
    relevance = models.FloatField()
