# encoding=utf-8

from __future__ import unicode_literals
from django.test import TestCase
from knowledge.utils.termstrie import TermsTrie
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


class TermsTrieTestCase(TestCase):

    def test_add_with_subnames_prefix(self):
        terms_trie = TermsTrie()
        terms_trie.add_with_subnames("Abraham Lincoln (politician)")
        self.assertEquals(terms_trie.get(['Abraham', 'Lincoln']), 'Abraham Lincoln (politician)')

    def test_add_with_subnames_suffix(self):
        terms_trie = TermsTrie()
        terms_trie.add_with_subnames("Abraham Lincoln")
        self.assertEquals(terms_trie.get(['Abraham', 'Lincoln']), 'Abraham Lincoln')
        self.assertEquals(terms_trie.get(['Lincoln']), 'Abraham Lincoln')

    def test_lowercase(self):
        terms_trie = TermsTrie()
        terms_trie.add("Mathematics", [("Mathematics", "NN")])
        self.assertEquals(terms_trie.get(['Mathematics']), 'Mathematics')
