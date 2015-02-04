from __future__ import unicode_literals
#from django.db import models
from abstract_component.models import Component


class Practicer(Component):
    """
    Model for practicer component.
    """

    BEHAVIORS_PATH = 'practice/practicer-behaviors/'

    @classmethod
    def get_behaviors_path(cls):
        return cls.BEHAVIORS_PATH

    def next_exercise(self, graded_exercises, accumulated_feedback):
        """
        Returns new exercise.

        Args:
            graded_exercises: collection of exercises and their grades
            accumulated_feedback: feedback from previous exercises to help us
                decide which exercise is best for the user
        Returns:
            new exercise || None if there is no exercise left
        """
        if not graded_exercises:
            return None
        behavior = self.get_behavior()
        exercise = behavior.next_exercise(graded_exercises,
            accumulated_feedback)
        return exercise

    def __unicode__(self):
        return '<Practicer {name}>'.format(name=self.name)
