from django.test import TestCase
from practice.models import Practicer
from exercises.models import Exercise


class PracticerTestCase(TestCase):
    def setUp(self):
        pass

    def test_next_exercise(self):
        # TODO: persistence???
        practicer = Practicer(behavior_name='fake', parameters={})
        exercise = practicer.next_exercise([Exercise(data={})], None)
        self.assertIsInstance(exercise, Exercise)
