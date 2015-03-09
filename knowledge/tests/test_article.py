# encoding=utf-8

from __future__ import unicode_literals
#from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from common.settings import SKIP_ONLINE_TESTS
from knowledge.models import Article
from knowledge.namespaces import TERM
from unittest import skipIf


class ArticleWithoutFixtureTestCase(TestCase):
    def setUp(self):
        Article.objects.create(
            topic=TERM['Pan_Tau'],
            content=Article.EMPTY_CONTENT)

    def test_article_retrieval(self):
        #a = Article.objects.first()
        #print a
        article = Article.objects.get(topic=TERM['Pan_Tau'])
        self.assertIsNotNone(article)
        self.assertEqual(article.topic, TERM['Pan_Tau'])
        self.assertEqual(article.get_name(), 'Pan Tau')
        #from json import dumps
        #print dumps(article.content)
        #print type(article.content)

    @skipIf(SKIP_ONLINE_TESTS, 'connection to Wikipedia public API')
    def test_new_article_from_wikipedia(self):
        topic = TERM['Prokop_the_Great']
        article, created = Article.objects.get_or_create(topic=topic)
        self.assertEqual(created, True)
        self.assertIsNotNone(article)
        self.assertEqual(article.topic, topic)
        terms = article.get_all_terms()
        self.assertIn(TERM['Prokop_the_Great'], terms)
        self.assertIn(TERM['Hussite_Wars'], terms)

    def test_create_content_from_text(self):
        text = """
Prokop or Prokop the Great (Czech: Prokop Veliký) (b. about 1380 – d. 30 May 1434 at Lipany) was one of the most prominent Hussite generals of the Hussite Wars. His name has also been given as Prokop Holý or Prokopius Rasus - Latin translation ("the Shaven," in allusion to his having received the tonsure in early life), Procopius the Great, and Andrew Procopius.


== Biography ==
Initially Prokop was a member of the Utraquists (the moderate wing of the Hussites) and was a married priest who belonged to an eminent family from Prague. He studied in Prague, and then traveled for several years in foreign countries. On his return to Bohemia, though a priest and continuing to officiate as such, he became the most prominent leader of the advanced Hussite or Taborite forces during the latter part of the Hussite wars. He was not the immediate successor of Jan Žižka as leader of the Taborites, as has been frequently stated, but he commanded the forces of Tabor when they obtained their great victories over the Germans and Catholics at Ústí nad Labem in 1426 and Domažlice in 1431. The crushing defeat that he inflicted on the crusaders of the Holy Roman Empire at Domažlice led to peace negotiations (1432) at Cheb between the Hussites and representatives of the Council of Basel.
He also acted as leader of the Taborites during their frequent incursions into Hungary and Germany, particularly when in 1429 a vast Bohemian army invaded Saxony and the territory of Nuremberg. The Hussites, however, made no attempt permanently to conquer German territory, and on 6 February 1430 Prokop concluded a treaty at Kulmbach with Frederick I, burgrave of Nuremberg, by which the Hussites engaged themselves to leave Germany. When the Bohemians entered into negotiations with Sigismund and the Council of Basel and, after prolonged discussions, resolved to send an embassy to the council, Prokop the Great was its most prominent member, reaching Basel on 4 January 1433. When the negotiations there for a time proved fruitless, Prokop with the other envoys returned to Bohemia, where new internal troubles broke out.
A Taborite army led by Prokop the Great besieged Plzeň, which was then in the hands of the Catholics. The discipline in the Hussite camp had, however, slackened in the course of prolonged warfare, and the Taborites encamped before Plzen revolted against Prokop, who therefore returned to Prague.
Probably encouraged by these dissensions among the men of Tabor, the Bohemian nobility, both Catholic and Utraquist, formed a league for the purpose of opposing radicalism, which through the victories of Tabor had acquired great strength in the Bohemian towns. The struggle began at Prague. Aided by the nobles, the citizens of the Old Town took possession of the more radical New Town, Prague, which Prokop unsuccessfully attempted to defend. Prokop now called to his aid Prokop the Lesser, who had succeeded him in the command of the Taborite army before Plzen. They jointly retreated eastward from Prague, and their forces, known as the army of the towns, met the army of the nobles between Kourim and Kolín in the Battle of Lipany (30 May 1434). The Taborites were decisively defeated, and both Prokops, Great and Lesser, perished in the battle.


== Notes ==


== References ==
 This article incorporates text from a publication now in the public domain: Chisholm, Hugh, ed. (1911). "Prokop". Encyclopædia Britannica (11th ed.). Cambridge University Press.
"""
        links = [u'Battle of Doma\u017elice', u'Battle of Lipany', u'Battle of \xdast\xed nad Labem', u'Cheb', u'Council of Basel', u'Czech language', u'Encyclop\xe6dia Britannica Eleventh Edition', u'Frederick I, Margrave of Brandenburg', u'German people', u'Holy Roman Empire', u'Hungary', u'Hussite', u'Hussite Wars', u'Jan \u017di\u017eka', u'Kol\xedn', u'Kourim', u'Kulmbach', u'New International Encyclopedia', u'New Town, Prague', u'Nuremberg', u'Plze\u0148', u'Prague', u'Prokop the Lesser', u'Public domain', u'Saxony', u'Sigismund, Holy Roman Emperor', u'Taborite', u'Tonsure', u'Utraquist', u'Prokop the Great']
        article = Article(topic=TERM['Prokop_the_Great'])
        article.create_content_from_text(text, links)
        #print article.content
        terms = article.get_all_terms()
        self.assertIn(TERM['Prokop_the_Great'], terms)
        self.assertIn(TERM['Hussite_Wars'], terms)
        sentences = article.get_sentences()
        # There is 19 usable sentences in the text
        #for s in sentences:
        #    print s
        #    print
        self.assertEqual(len(sentences), 19)

    #def test_nonexisting_article_retrieval(self):
    #    with self.assertRaises(ObjectDoesNotExist):
    #        Article.objects.get(topic=TERM['Mr_Alpha'])

    #def test_content_retrieval(self):
    #    article = Article.objects.get(topic=TERM['Pan_Tau'])
    #    self.assertEqual(article.content, '[]')


class ArticleWithFixtureTestCase(TestCase):
    fixtures = ['lincoln-article-short.xml']

    def setUp(self):
        self.topic = TERM['Abraham_Lincoln']
        self.article = Article.objects.get(topic=self.topic)
        #self.maxDiff = None

    def test_parsing_article_from_DB(self):
        self.assertEqual(self.article.get_name(), 'Abraham Lincoln')
        self.assertEqual(self.article.topic, self.topic)
        self.assertEqual(len(self.article.get_sentences()), 2)

    def test_get_all_terms(self):
        terms = self.article.get_all_terms()
        self.assertIn(TERM['Abraham_Lincoln'], terms)
        self.assertIn(TERM['American_Civil_War'], terms)
