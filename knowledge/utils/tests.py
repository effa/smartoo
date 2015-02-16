"""
Knowledge utilities tests
"""

from __future__ import unicode_literals
from django.test import TestCase
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import RDFS, TERM, XSD, DC, ONTOLOGY
#from knowledge.utils.sparql import label
from rdflib import Literal

# TODO: testy presunout o uroven vyse


class SparqlTestCase(TestCase):
    def setUp(self):
        self.knowledge_graph = KnowledgeGraph()
        self.henry8 = TERM['Henry_VIII_of_England']
        self.henry5 = TERM['Henry_V_of_England']
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

    # TODO
