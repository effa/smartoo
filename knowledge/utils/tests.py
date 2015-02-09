"""
Knowledge utilities tests
"""

from __future__ import unicode_literals
from django.test import TestCase
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import RDFS, RESOURCE, XSD, DC, ONTOLOGY
from knowledge.utils.sparql import label
from rdflib import Literal


class SparqlTestCase(TestCase):
    def setUp(self):
        self.knowledge_graph = KnowledgeGraph()
        self.henry8 = RESOURCE['Henry_VIII_of_England']
        self.henry5 = RESOURCE['Henry_V_of_England']
        self.knowledge_graph.add((self.henry8,
            RDFS['label'],
            Literal('Henry VIII')))
        self.knowledge_graph.add((self.henry8,
            DC['description'],
            Literal('King of England')))
        self.knowledge_graph.add((self.henry5,
            DC['description'],
            Literal('King of England')))
        self.knowledge_graph.add((self.henry8,
            ONTOLOGY['birthDate'],
            Literal('1491-06-28', datatype=XSD.date)))

    def test_label(self):
        self.assertEqual(label(self.henry8, self.knowledge_graph), 'Henry VIII')
        self.assertEqual(label(self.henry5, self.knowledge_graph), 'Henry V of England')
        self.assertIsNone(label(self.henry5, self.knowledge_graph, fallback_guess=False))
