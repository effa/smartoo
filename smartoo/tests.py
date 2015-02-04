from django.test import TestCase
from knowledge.models import Vertical, Topic, KnowledgeGraph, KnowledgeBuilder
from exercises.models import Exercise, ExercisesCreator
from exercises.models import ExerciseGrades, ExercisesGrader
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
        self.assertIsNotNone(session)
        self.assertEqual(session.topic, self.topic)
        self.assertIsInstance(session.knowledge_builder, KnowledgeBuilder)
        self.assertIsInstance(session.exercises_creator, ExercisesCreator)
        self.assertIsInstance(session.exercises_grader, ExercisesGrader)
        self.assertIsInstance(session.practicer, Practicer)
        self.assertEqual(session.finnished, False)

    def test_build_knowledge(self):
        session = Session.objects.create_with_components(self.topic)
        session.build_knowledge()
        knowledge_graph = KnowledgeGraph.objects.all().first()
        self.assertIsNotNone(knowledge_graph)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)

    def test_create_graded_exercises(self):
        session = Session.objects.create_with_components(self.topic)
        # TODO: lepsi by bylo tam graf vlozit manualne (abychom se zbavili
        # zavislosti na uspechu build_knowledge()
        session.build_knowledge()
        session.create_graded_exercises()
        exercises = Exercise.objects.all()
        grades = ExerciseGrades.objects.all()
        # check that exercises and grades were stored
        self.assertGreater(len(exercises), 0,
            "No exercises were stored.")
        self.assertGreater(len(grades), 0,
            "No grades were stored.")
        self.assertEqual(len(exercises), len(grades),
            "The number of stored grades and exercises is different.")
        # TODO: nejake dalsi asserty??

    # TODO: test pro vyber cviceni
