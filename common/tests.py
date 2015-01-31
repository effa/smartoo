from __future__ import unicode_literals
from django.test import TestCase
from common.utils.wiki import uri_to_name, name_to_uri


class WikiUtilsTestCase(TestCase):

    def test_uri_to_name(self):
        """
        URIs are correctly transformed to names.
        """
        for uri, expected_name in [
                ('http://en.wikipedia.org/wiki/USA', 'USA'),
                ('http://cs.wikipedia.org/wiki/Pan_Tau', 'Pan Tau'),
                ('http://en.wikipedia.org/wiki/A', 'A')]:
            self.assertEqual(uri_to_name(uri), expected_name)

    def test_name_to_uri_en(self):
        """
        Names with default (English) language are correctly transformed to URI
        """
        for name, expected_uri in [
                ('USA', 'http://en.wikipedia.org/wiki/USA'),
                ('word', 'http://en.wikipedia.org/wiki/Word'),
                ('Pan Tau', 'http://en.wikipedia.org/wiki/Pan_Tau'),
                ('a b c', 'http://en.wikipedia.org/wiki/A_b_c')]:
            self.assertEqual(name_to_uri(name), expected_uri)

    def test_name_to_uri_language(self):
        """
        Names with non-default language are correctly transformed to URI
        """
        for name, lang, expected_uri in [
                ('USA', 'en', 'http://en.wikipedia.org/wiki/USA'),
                ('Pan Tau', 'cs', 'http://cs.wikipedia.org/wiki/Pan_Tau'),
                ('Pan Tau', 'sk', 'http://sk.wikipedia.org/wiki/Pan_Tau')]:
            self.assertEqual(name_to_uri(name, lang), expected_uri)
