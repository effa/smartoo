# encoding=utf-8

from __future__ import unicode_literals
#from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from knowledge.models import KnowledgeBuilder, Article
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import RDF, RDFS, ONTOLOGY, SMARTOO, TERM
#from knowledge.utils.sparql import prepared_query
from rdflib import Graph, Literal, Namespace


class KnowledgeGraphWithoutFixtureTestCase(TestCase):
    # NOTE: to speed up tests, I have factor out test which doesn't need
    # loading fixtures into DB

    def test_label(self):
        knowledge_graph = KnowledgeGraph()
        tomE = TERM['Tom_E']
        tomF = TERM['Tom_F']
        knowledge_graph.add((tomE, RDFS['label'], Literal('Tom')))
        self.assertEqual(knowledge_graph.label(tomE), 'Tom')
        self.assertEqual(knowledge_graph.label(tomF), 'Tom F')
        self.assertIsNone(knowledge_graph.label(tomF, fallback_guess=False))

    def test_types_set_manually(self):
        knowledge_graph = KnowledgeGraph()
        termA = TERM['A']
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        types = knowledge_graph.types(termA)
        self.assertIn(SMARTOO['term'], types)
        self.assertNotIn(ONTOLOGY['Activity'], types)

    def test_terms_similarity(self):
        knowledge_graph = KnowledgeGraph()
        termA = TERM['A']
        termB = TERM['B']
        # adding types and checking similarity after each step
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.06241874674751258)
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.06241874674751258)
        knowledge_graph.add((termB, RDF['type'], SMARTOO['term']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.06241874674751258)
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Agent']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.06241874674751258)
        knowledge_graph.add((termB, RDF['type'], ONTOLOGY['Agent']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.12435300177159614)
        knowledge_graph.add((termB, RDF['type'], ONTOLOGY['Person']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.12435300177159614)
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Person']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.18533319990813935)

    def test_all_terms(self):
        knowledge_graph = KnowledgeGraph()
        termA = TERM['A']
        termB = TERM['B']
        termC = TERM['C']
        self.assertEqual(len(knowledge_graph.all_terms), 0)
        knowledge_graph.add((termA, SMARTOO['sth'], SMARTOO['sth']))
        # we use implicit definition of terms so there should alredy be 1
        self.assertEqual(len(knowledge_graph.all_terms), 1)
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        self.assertEqual(len(knowledge_graph.all_terms), 1)
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Agent']))
        self.assertEqual(len(knowledge_graph.all_terms), 1)
        knowledge_graph.add((termB, RDF['type'], SMARTOO['term']))
        self.assertEqual(len(knowledge_graph.all_terms), 2)
        # also objects can be terms
        knowledge_graph.add((SMARTOO['sth'], SMARTOO['sth'], termC))
        self.assertEqual(len(knowledge_graph.all_terms), 3)
        self.assertEqual(sorted(knowledge_graph.all_terms), [termA, termB, termC])


class KnowledgeGraphTestCase(TestCase):
    fixtures = ['lincoln-components-article-global_knowledge.xml']

    def setUp(self):
        # get fake knowledge builder (already in DB: see fixture)
        self.knowledge_builder = KnowledgeBuilder.objects.get(
            behavior_name='fake', parameters={})

    def test_serialization_deserialization(self):
        # create knowledge graph and serialize it
        graph = Graph()
        NS = Namespace('http://example.com/test/')
        graph.bind('ns', NS)
        topic = TERM['Tom']
        graph.add((topic, NS['likes'], Literal('apples')))
        KnowledgeGraph.objects.create(
            knowledge_builder=self.knowledge_builder,
            topic=topic,
            graph=graph)
        # graph retrieval
        knowledge_graph = KnowledgeGraph.objects.get(
            topic=topic)
        graph2 = knowledge_graph.graph
        # check that the graph after serialization-deserialization is still the
        # same as it was
        #print graph2.serialize(format='turtle')
        #print graph.serialize(format='turtle')
        self.assertTrue(graph2.isomorphic(graph))

    def test_types_of_term(self):
        term = TERM['Abraham_Lincoln']
        knowledge_graph = KnowledgeGraph.objects.get(topic=term)
        self.assertIsInstance(knowledge_graph.types_of_term, dict)
        self.assertIn(term, knowledge_graph.types_of_term)

    def test_terms_of_type(self):
        term = TERM['Abraham_Lincoln']
        knowledge_graph = KnowledgeGraph.objects.get(topic=term)
        self.assertIsInstance(knowledge_graph.terms_of_type, dict)
        self.assertIn(ONTOLOGY['Person'], knowledge_graph.terms_of_type)
        self.assertIn(term,
            knowledge_graph.terms_of_type[ONTOLOGY['Person']])

    def test_types(self):
        term = TERM['Abraham_Lincoln']
        knowledge_graph = KnowledgeGraph.objects.get(topic=term)
        types = knowledge_graph.types(term)
        self.assertIsInstance(types, set)
        self.assertIn(ONTOLOGY['Agent'], types)
        self.assertIn(ONTOLOGY['Person'], types)
        self.assertNotIn(ONTOLOGY['Activity'], types)

    def test_add_related_global_knowledge(self):
        topic = TERM['Abraham_Lincoln']
        article = Article.objects.get(topic=topic)
        knowledge_graph = KnowledgeGraph(topic=topic)
        knowledge_graph.add_related_global_knowledge(article, online=False)
        #print knowledge_graph
        self.assertEqual(len(knowledge_graph.graph), 762)
        # there are 28 terms in article + Lincoln graph
        self.assertEqual(len(set(knowledge_graph.get_subjects())), 28)
        # test few triples in the graph
        self.assertIn(ONTOLOGY['Person'],
            knowledge_graph.types(TERM['Abraham_Lincoln']))
        self.assertIn(ONTOLOGY['Person'],
            knowledge_graph.types(TERM['Andrew_Johnson']))
        self.assertEqual(
            knowledge_graph.label(TERM['Tad_Lincoln'], fallback_guess=False),
            'Tad Lincoln')
