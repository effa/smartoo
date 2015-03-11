# encoding=utf-8

"""
Special test module to try components which are currently under development.
These tests are not meant to be fully automated, it's rather a check that there
are no syntax errors in currently developed behavior and it behaves as expected
"""

from django.test import TestCase

from unittest import skipIf

from knowledge.namespaces import TERM
from knowledge.models import KnowledgeBuilder
from exercises.models import ExercisesCreator
from exercises.models import ExercisesGrader
from exercises.models import GradedExercise, Exercise
from practice.models import Practicer
from smartoo.models import Session

# skip flag: whether to execute these special tests or not
SKIP = False


class ComponentsTestCase(TestCase):
    fixtures = ['initial-fixture.xml']

    def setUp(self):
        self.topic = TERM['Abraham_Lincoln']
        #self.session = Session.objects.create_with_components(self.topic)
        self.session = Session(topic=self.topic)
        # ------------------------------------------------------------------
        # components to test
        # ------------------------------------------------------------------
        self.session.knowledge_builder = KnowledgeBuilder.objects.get(
            behavior_name='quasi',
            parameters={})
        self.session.exercises_creator = ExercisesCreator.objects.get(
            behavior_name='quasi',
            parameters={})
        self.session.exercises_grader = ExercisesGrader.objects.get(
            behavior_name='simple',
            parameters={})
        self.session.practicer = Practicer.objects.get(
            behavior_name='simple',
            parameters={})
        # ------------------------------------------------------------------
        self.session.save()

    @skipIf(SKIP, "special components behavior test")
    def test_components(self):
        # NOTE: there will whatever I want to test right now

        # knowledge building
        self.session.build_knowledge()
        #print self.session.get_knowledge_graph()

        # exercises creating
        #self.session.create_graded_exercises()
        #print '***'
        #for exercise in self.session.get_graded_exercises():
        #    print exercise

        # fake exercises (to test pracicing only)
        GradedExercise.objects.create(
            exercise=Exercise.objects.create(data='B',
                knowledge_graph=self.session.get_knowledge_graph(),
                exercises_creator=self.session.exercises_creator),
            exercises_grader=self.session.exercises_grader,
            difficulty=0.5,
            correctness=0.5,
            relevance=0.2)
        GradedExercise.objects.create(
            exercise=Exercise.objects.create(data='A',
                knowledge_graph=self.session.get_knowledge_graph(),
                exercises_creator=self.session.exercises_creator),
            exercises_grader=self.session.exercises_grader,
            difficulty=0.5,
            correctness=0.5,
            relevance=0.4)

        # practicing
        exercise = self.session.next_exercise()
        print exercise
        self.session.provide_feedback({
            'pk': exercise.pk,
            'answered': True,
            'correct': True,
            'invalid': False,
            'irrelevant': False
        })
