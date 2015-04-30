from __future__ import unicode_literals
from django.test import TestCase
from knowledge.models import KnowledgeBuilder, KnowledgeGraph
from knowledge.namespaces import RDF, SMARTOO, ONTOLOGY, TERM, LABEL
from exercises.models import Exercise, ExercisesCreator
from exercises.models import GradedExercise, ExercisesGrader
from exercises.utils.distractors import generate_similar_terms, create_choice_list
from exercises.utils.difficulty import difficulty_normalization
from rdflib import Literal


class ExercisesCreatorTestCase(TestCase):
    def setUp(self):
        # create a topic_uri, knowledge builder and knowledge graph
        self.topic = 'http://dbpedia.org/resource/Pan_Tau'
        self.knowledge_builder = KnowledgeBuilder.objects.create(
            behavior_name='fake',
            parameters={"alpha": 0.5})
        self.knowledge_graph = KnowledgeGraph.objects.create(
            topic=self.topic,
            knowledge_builder=self.knowledge_builder)

    def test_create_exercises(self):
        creator = ExercisesCreator.objects.create(
            behavior_name='fake', parameters={})
        # check exercises yielding
        exercises_count = 0
        for exercise in creator.create_exercises(self.knowledge_graph):
            self.assertIsInstance(exercise, Exercise)
            self.assertIsInstance(exercise.data, dict)
            self.assertTrue('question' in exercise.data)
            self.assertIsInstance(exercise.data['question'], basestring)
            exercises_count += 1
        # check that nonzerou number of exercises was yielded
        self.assertGreater(exercises_count, 0)
        # check that all the exercises were stored
        self.assertEqual(len(Exercise.objects.all()), exercises_count)


class ExercisesGraderTestCase(TestCase):
    def setUp(self):
        # create a topic_uri, knowledge builder and knowledge graph
        self.topic = 'http://dbpedia.org/resource/Pan_Tau'
        self.knowledge_builder = KnowledgeBuilder.objects.create(
            behavior_name='fake',
            parameters={"alpha": 0.5})
        self.knowledge_graph = KnowledgeGraph.objects.create(
            topic=self.topic,
            knowledge_builder=self.knowledge_builder)
        self.exercises_creator = ExercisesCreator.objects.create(
            behavior_name='fake', parameters={})

    def test_create_graded_exercises(self):
        exercises_grader = ExercisesGrader.objects.create(
            behavior_name='fake', parameters={})
        # create grades (and store them)
        exercises_grader.create_graded_exercises(
            self.knowledge_graph, self.exercises_creator)
        # check that all the exercises and grades were stored
        self.assertGreater(len(Exercise.objects.all()), 0)
        self.assertGreater(len(GradedExercise.objects.all()), 0)
        self.assertEqual(len(Exercise.objects.all()),
            len(GradedExercise.objects.all()))
        # check that grades were saved and can be retrieved
        grades = GradedExercise.objects.all().first()
        self.assertIsInstance(grades.difficulty, float)


class DistractorsUtilsTestCase(TestCase):
    def setUp(self):
        pass

    def test_generate_similar_terms(self):
        knowledge_graph = KnowledgeGraph()
        termA = TERM['A']
        termB = TERM['B']
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        knowledge_graph.add((termB, RDF['type'], SMARTOO['term']))
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Agent']))
        knowledge_graph.add((termB, RDF['type'], ONTOLOGY['Agent']))
        terms = generate_similar_terms(termA, knowledge_graph, 4)
        # as the generating method might be random, we cant's say a term is in
        # the result for sure, so we just check that correct number of terms
        # was returned, that it doesn't contains any duplicats and that the
        # root term itself is not between distractors
        self.assertEqual(len(terms), 4)
        self.assertEqual(len(set(terms)), 4)
        self.assertNotIn(termA, terms)
        terms = generate_similar_terms(termA, knowledge_graph, 5)
        self.assertEqual(len(terms), 5)
        self.assertEqual(len(set(terms)), 5)
        self.assertNotIn(termA, terms)

    def test_create_choice_list(self):
        knowledge_graph = KnowledgeGraph()
        henry = TERM['Henry_VIII_of_England']
        edward = TERM['Edward_VI_of_England']
        elizabeth = TERM['Elizabeth_of_York']
        knowledge_graph.add((henry, LABEL, Literal('Henry VIII')))
        knowledge_graph.add((edward, LABEL, Literal('Edward VI')))
        # it should also work without having some terms in the graph (using
        # label fallback)
        #knowledge_graph.add((elizabeth, LABEL, Literal('Elizabeth of York')))
        choices = create_choice_list([henry, edward, elizabeth], knowledge_graph)
        self.assertEqual(sorted(choices), ['Edward VI', 'Elizabeth of York', 'Henry VIII'])


class DifficultyUtilsTestCase(TestCase):

    def test_difficulty_normalization(self):
        self.assertEqual(difficulty_normalization(0), -2)
        self.assertEqual(difficulty_normalization(1), 2)
        self.assertAlmostEqual(difficulty_normalization(0.5), 0)
        self.assertAlmostEqual(difficulty_normalization(0.75), 1)
        self.assertAlmostEqual(difficulty_normalization(0.125), -1.5)
