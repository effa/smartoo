# encoding=utf-8

"""
Special test module to try components which are currently under development.
These tests are not meant to be fully automated, it's rather a check that there
are no syntax errors in currently developed behavior and it behaves as expected
"""

from django.test import TestCase

from unittest import skipIf

from knowledge.models import KnowledgeBuilder
from exercises.models import ExercisesCreator
from exercises.models import ExercisesGrader
from practice.models import Practicer
from smartoo.models import Session

# skip flag: whether to execute these special tests or not
SKIP = True


class ComponentsTestCase(TestCase):
    fixtures = ['initial-lincoln.xml']

    def setUp(self):
        self.topic_uri = 'http://dbpedia.org/resource/Abraham_Lincoln'
        self.session = Session(topic_uri=self.topic_uri)
        # ------------------------------------------------------------------
        # components to test
        # ------------------------------------------------------------------
        self.session.knowledge_builder = KnowledgeBuilder.objects.get(
            behavior_name='simple',
            parameters={})
        self.session.exercises_creator = ExercisesCreator.objects.get(
            behavior_name='quasi',
            parameters={})
        self.session.exercises_grader = ExercisesGrader.objects.get(
            behavior_name='fake',
            parameters={})
        self.session.practicer = Practicer.objects.get(
            behavior_name='fake',
            parameters={})
        # ------------------------------------------------------------------
        self.session.save()

    @skipIf(SKIP, "special components behavior test")
    def test_components(self):
        # there will whatever I want to test right now
        self.session.build_knowledge()
        #print self.session.get_knowledge_graph()
        self.session.create_graded_exercises()
        for exercise in self.session.get_graded_exercises():
            print exercise