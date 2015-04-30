from django.test import TestCase
from exercises.models import Exercise, GradedExercise
from practice.models import Practicer
from practice.utils.logistic_model import correct_answer_probability, practice_likelihood, estimate_knowledge
from practice.utils.target_probability_adjustment import compute_target_probability

from math import log


class PracticerTestCase(TestCase):

    def test_next_exercise(self):
        exercise = Exercise()
        graded_exercise = GradedExercise(exercise=exercise)
        practicer = Practicer(behavior_name='fake', parameters={})
        next_exercise = practicer.next_exercise([graded_exercise], None, None)
        self.assertIsInstance(next_exercise, GradedExercise)
        self.assertEqual(next_exercise, graded_exercise)


class LogisticModelTestCase(TestCase):

    def test_correct_answer_probability(self):
        self.assertAlmostEqual(correct_answer_probability(0.8, 0.8), 0.625)
        self.assertAlmostEqual(correct_answer_probability(1.2, 1.2), 0.625)
        self.assertAlmostEqual(correct_answer_probability(1.2, 1.2 + log(2)), 0.5)
        self.assertAlmostEqual(correct_answer_probability(1.2, 0.4), 0.7674808608457)
        self.assertAlmostEqual(correct_answer_probability(1.2, -0.4), 0.8740137888504)

    def test_practice_likelihood(self):
        self.assertAlmostEqual(practice_likelihood([1.2], [], 1.2), 0.625)
        self.assertAlmostEqual(practice_likelihood([], [1.2], 1.2), 0.375)
        self.assertAlmostEqual(practice_likelihood([1.2, 1.2, 1.2], [], 1.2), 0.244140625)
        self.assertAlmostEqual(practice_likelihood([1.2], [1.2], 1.2), 0.234375)
        self.assertAlmostEqual(practice_likelihood([-0.4, 0.4], [0.4, 1.2], 1.2), 0.05848921767463701)

    def test_compute_target_probability(self):
        self.assertAlmostEqual(compute_target_probability(0.75, 0.75, 4), 0.75)
        self.assertAlmostEqual(compute_target_probability(0.75, 1, 100), 0.0, places=3)
        self.assertAlmostEqual(compute_target_probability(0.75, 1, 10), 0.0, places=1)
        self.assertAlmostEqual(compute_target_probability(0.75, 0, 100), 1.0, places=3)
        self.assertAlmostEqual(compute_target_probability(0.75, 0, 10), 1.0, places=1)
        self.assertAlmostEqual(compute_target_probability(0.75, 0.875, 5), 0.375, delta=0.15)

    def test_estimate_knowledge(self):
        self.assertAlmostEqual(estimate_knowledge([0] * 10, [0] * 10), -0.7, places=1)
        self.assertAlmostEqual(estimate_knowledge([0.5, 1.0, 1.5], [1.9]), 1.6, places=1)
        self.assertAlmostEqual(estimate_knowledge([0.5, 1.0], [1.7, 1.9]), 0.7, places=1)
