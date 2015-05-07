# encoding=utf-8

"""
Special test module to try components which are currently under development.
These tests are not meant to be fully automated, it's rather a check that there
are no syntax errors in currently developed behavior and it behaves as expected
"""

from django.test import TestCase

from unittest import skipIf

from knowledge.namespaces import TERM
from knowledge.models import KnowledgeBuilder, Article
from exercises.models import ExercisesCreator
from exercises.models import ExercisesGrader
from exercises.models import GradedExercise, Exercise
from practice.models import Practicer
from smartoo.models import Session

# skip flag: whether to execute these special tests or not
SKIP = True


class ComponentsTestCase(TestCase):
    fixtures = ['initial-fixture.xml']

    def setUp(self):
        self.topic = TERM['Abraham_Lincoln']
        Article.objects.create(topic=self.topic, content=Article.EMPTY_CONTENT)
        #self.session = Session.objects.create_with_components(self.topic)
        self.session = Session(topic=self.topic)
        # ------------------------------------------------------------------
        # components to test
        # ------------------------------------------------------------------
        self.session.knowledge_builder = KnowledgeBuilder.objects.get(pk=4)  # fake
        self.session.exercises_creator = ExercisesCreator.objects.get(pk=1)
        self.session.exercises_grader = ExercisesGrader.objects.get(pk=1)
        self.session.practicer = Practicer.objects.get(pk=1)
        # ------------------------------------------------------------------
        self.session.save()

    @skipIf(True or SKIP, "special components behavior test")
    def test_components(self):
        # NOTE: there will whatever I want to test right now

        # knowledge building
        self.session.build_knowledge()
        #print self.session.get_knowledge_graph()

    @skipIf(SKIP, "special components behavior test")
    def test_practicing_only(self):
        # knowledge building
        self.session.build_knowledge()

        for difficulty in [-1.2 + 0.1 * k for k in range(32)]:
            GradedExercise.objects.create(
                exercise=Exercise.objects.create(data='Q',
                    semantics={'term-pairs': []},
                    knowledge_graph=self.session.get_knowledge_graph(),
                    exercises_creator=self.session.exercises_creator),
                exercises_grader=self.session.exercises_grader,
                difficulty=difficulty,
                correctness=0.5,
                relevance=0.5)

        for i in range(10):

            # practicing
            exercise = self.session.next_exercise()
            print exercise

            print 'Correct answer? ',
            answer = bool(int(raw_input()))

            self.session.provide_feedback({
                'pk': exercise.pk,
                'answered': True,
                'correct': answer,
                'invalid': False,
                'irrelevant': False
            })


class ComponentsSelectorTestCase(TestCase):
    fixtures = ['session-history.xml']

    def setUp(self):
        self.topic = TERM['Abraham_Lincoln']

    @skipIf(True or SKIP, "special components selecting test")
    def test_selector(self):
        session = Session.objects.create_with_components(self.topic)
        self.assertIsNotNone(session)
        print session
