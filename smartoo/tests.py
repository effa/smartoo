from django.test import TestCase
from knowledge.models import Vertical, Topic, KnowledgeBuilder
from exercises.models import ExercisesCreator, ExercisesGrader
from practice.models import Practicer
from smartoo.models import Session


class SessiontTestCase(TestCase):
    def setUp(self):
        # create test vertical and topic
        vertical = Vertical.objects.create(content='test line')
        self.topic = Topic.objects.create(
            uri='http://en.wikipedia.org/wiki/Pan_Tau',
            vertical=vertical)
        # create fake components in the DB
        KnowledgeBuilder.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})
        ExercisesCreator.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})
        ExercisesGrader.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})
        Practicer.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})

    def test_create_session(self):
        session = Session.objects.create_with_components(self.topic)

    # TODO: testy na jednotlive akce (tvorba znalosti, tvorba cviceni, vyber
    # cviceni
