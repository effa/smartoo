from django.test import TestCase
from practice.models import Practicer
from exercises.models import Exercise, GradedExercise


class PracticerTestCase(TestCase):

    def test_next_exercise(self):
        exercise = Exercise()
        practicer = Practicer(behavior_name='fake', parameters={})
        next_exercise = practicer.next_exercise([GradedExercise(exercise=exercise)], None)
        self.assertIsInstance(exercise, Exercise)
        self.assertEqual(next_exercise, exercise)
