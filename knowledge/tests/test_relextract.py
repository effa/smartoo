# encoding=utf-8

from __future__ import unicode_literals
from django.test import TestCase
#from knowledge.namespaces import TERM
#from knowledge.models import Article
#from knowledge.utils.relextract import RuleBasedRelationExtractor


class RuleBasedRelationExtractorTestCase(TestCase):
    pass

    #def setUp(self):
    #    # TODO: potreba upravit, aktualne je jiny format obsahu clanku (viz
    #    # models.py)
    #    article = Article(content={u'sentences': [
    #        {u'sentence': u'''(S\n  (NNP Lincoln)\n  (VBD averted)\n (JJ potential)\n
    #        (JJ British)\n  (NN intervention)\n  (IN in)\n(DT the)\n  (NN war)\n
    #        (IN by)\n  (NN defusing)\n  (DT the)\n  (TERM (NNP Trent) (NNP Affair))\n
    #        (IN in)\n  (JJ late)\n  (CD 1861)\n  (. .))''',
    #        u'terms': ['Trent Affair']}]})
    #    self.sentences = article.get_sentences()

    #def test_BLABLA_rule(self):
    #    extractor = RuleBasedRelationExtractor('')
    #    for sentence in self.sentences:
    #        result = extractor.extract_relation(sentence)
    #        self.assertIsNone(result)
