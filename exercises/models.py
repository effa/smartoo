from django.db import models
from knowledge.models import KnowledgeBuilder

# TODO: component ...


class Exercise(models.Model):
    """
    Base class for an exercise
    """
    question = models.TextField()
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    #exercises_creator = models.ForeignKey(ExercisesCreator)
    # possibly: image, map, type (multichoice/free answer/...), ...


class Options(models.Model):
        exercise = models.ForeignKey(Exercise)
        correct = models.BooleanField(default=True)
        string = models.CharField(max_length=500)  # possibly declined etc.
        # + reference na term do Knowledge (potreba semantickych informaci
        #   kvuli ohodnoceni otazky


class ExerciseGrade(models.Model):
    exercise = models.ForeignKey(Exercise)
    #exercise_grader = models.ForeignKey(ExerciseGrader)
