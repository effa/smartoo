from __future__ import unicode_literals
from django.db import models
from abstract_component.models import Component
from knowledge.models import KnowledgeBuilder


# ---------------------------------------------------------------------------
#  Components
# ---------------------------------------------------------------------------

class ExercisesCreator(Component):
    """
    Model for exercises creator component.
    """

    BEHAVIORS_PATH = 'exercises/exercises-creator-behaviors'

    @classmethod
    def get_behaviors_path(cls):
        return cls.BEHAVIORS_PATH

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
    Base class for an exercise
    """
    question = models.TextField()
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    exercises_creator = models.ForeignKey(ExercisesCreator)
    # possibly: image, map, type (multichoice/free answer/...), ...


class Options(models.Model):
        exercise = models.ForeignKey(Exercise)
        correct = models.BooleanField(default=True)
        string = models.CharField(max_length=500)  # possibly declined etc.
        # + reference na term do Knowledge (potreba semantickych informaci
        #   kvuli ohodnoceni otazky


class ExerciseGrades(models.Model):
    exercise = models.ForeignKey(Exercise)
    #exercise_grader = models.ForeignKey(ExerciseGrader)

    # difficulty: probability that a user doesn't know the correct answer
    difficulty = models.FloatField()

    # probability that the question is correct syntactically, semantically, ...
    correctness = models.FloatField()

    # relevance: probability of the question being relevant to the topic
    relevance = models.FloatField()
