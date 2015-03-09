# encoding=utf-8

from __future__ import unicode_literals
from django.test import TestCase
from common.settings import SKIP_ONLINE_TESTS
from knowledge.models import KnowledgeBuilder
from knowledge.models import KnowledgeGraph, GlobalKnowledge
from knowledge.namespaces import TERM
from unittest import skipIf


class GlobalKnowledgeEmptyDBTestCase(TestCase):
    """
    Tests GlobalKnowledge class when the DB is empty.
    """
    def setUp(self):
        self.global_knowledge = GlobalKnowledge()

    def test_get_global_knowledge_builder(self):
        self.assertIsNotNone(self.global_knowledge.knowledge_builder)
        self.assertIsInstance(self.global_knowledge.knowledge_builder,
            KnowledgeBuilder)
        global_knowledge2 = GlobalKnowledge()
        self.assertIsNotNone(global_knowledge2.knowledge_builder)
        self.assertIsInstance(global_knowledge2.knowledge_builder,
            KnowledgeBuilder)
        self.assertEqual(self.global_knowledge.knowledge_builder,
            global_knowledge2.knowledge_builder)

    @skipIf(SKIP_ONLINE_TESTS, 'connection to DBpedia public endpoint')
    def test_get_graph(self):
        term = TERM['Henry_VIII_of_England']
        knowledge_graph = self.global_knowledge.get_graph(term)
        self.assertIsNotNone(knowledge_graph)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)
        self.assertGreater(len(knowledge_graph.graph), 0)
        #print knowledge_graph
        #print 'number of triples:', len(knowledge_graph.graph)
        # now check if it works when it's already in DB
        knowledge_graph2 = self.global_knowledge.get_graph(term)
        self.assertEqual(knowledge_graph, knowledge_graph2)


class GlobalKnowledgeTestCase(TestCase):
    """
    Tests GlobalKnowledge class when the DB is populated.
    """
    fixtures = ['henry8-knowledge-graph-by-global_knowledge.xml']

    def setUp(self):
        self.global_knowledge = GlobalKnowledge()

    def test_get_global_knowledge_builder(self):
        self.assertIsNotNone(self.global_knowledge.knowledge_builder)
        self.assertIsInstance(self.global_knowledge.knowledge_builder, KnowledgeBuilder)

    def test_get_graph(self):
        term = TERM['Henry_VIII_of_England']
        knowledge_graph = self.global_knowledge.get_graph(term, online=False)
        self.assertIsNotNone(knowledge_graph)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)
        self.assertGreater(len(knowledge_graph.graph), 0)
        #print knowledge_graph
        #print 'number of triples:', len(knowledge_graph.graph)

#    #def test_label(self):
#    #    henry = TERM['Henry_VIII_of_England']
#    #    label = self.global_knowledge.label(henry, fallback_guess=False)
#    #    self.assertEqual(label, 'Henry VIII of England')

#    #    self.assertEqual(next(iter(result)), 'Henry VIII')
