# encoding=utf-8

from __future__ import unicode_literals
from django.test import TestCase
from knowledge.namespaces import TERM
from rdflib import URIRef


class TermTestCase(TestCase):
    def setUp(self):
        pass

    def test_term_properties(self):
        term = TERM['Pan_Tau']
        self.assertIsInstance(term, unicode)
        self.assertIsInstance(term, URIRef)
        r = TERM['Pan_Tau']
        self.assertEqual(unicode(term), unicode(r))
        self.assertEqual(term, term)
        self.assertEqual(r, term)
