# encoding=utf-8

from __future__ import unicode_literals
#from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from common.settings import SKIP_ONLINE_TESTS
from knowledge.models import KnowledgeBuilder, Article
from knowledge.models import KnowledgeGraph, GlobalKnowledge
from knowledge.namespaces import RDF, RDFS, ONTOLOGY, SMARTOO, TERM
#from knowledge.utils.sparql import prepared_query
from rdflib import Graph, Literal, Namespace, URIRef
from unittest import skipIf


#TODO: rozdelit do vice souboru (podbalik pro testy)


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
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0)
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0)
        knowledge_graph.add((termB, RDF['type'], SMARTOO['term']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0)
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Agent']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0)
        knowledge_graph.add((termB, RDF['type'], ONTOLOGY['Agent']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.5)
        knowledge_graph.add((termB, RDF['type'], ONTOLOGY['Person']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.5)
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Person']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 2.0 / 3)

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


class KnowledgeBuilderTestCase(TestCase):
    def setUp(self):
        self.topic = TERM['Pan_Tau']
        Article.objects.create(
            topic=self.topic,
            content='test')

    def test_create_two_builders_with_same_name(self):
        try:
            KnowledgeBuilder.objects.create(
                behavior_name='fake',
                parameters={"alpha": 0.5})
            KnowledgeBuilder.objects.create(
                behavior_name='fake',
                parameters={"alpha": 1.0})
        except:
            self.fail('Creating two components with the same behavior should'
                + ' be possible')

    def test_retrieval(self):
        # store knowledge builder to DB
        knowledge_builder = KnowledgeBuilder.objects.create(
            behavior_name='fake',
            parameters={"alpha": 0.5})
        key = knowledge_builder.pk
        # and check if everything is OK after retrieval
        knowledge_builder = KnowledgeBuilder.objects.get(pk=key)
        self.assertEqual(knowledge_builder.behavior_name, 'fake')
        self.assertEqual(knowledge_builder.parameters, {"alpha": 0.5})

    def test_behavior_instance(self):
        knowledge_builder = KnowledgeBuilder(behavior_name='fake',
            parameters={"alpha": 0.5})
        behavior = knowledge_builder.get_behavior()
        knowledge_graph = behavior.build_knowledge_graph(None)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)
        self.assertAlmostEqual(behavior.get_parameter('alpha'), 0.5)

    def test_build_knowledge(self):
        knowledge_builder = KnowledgeBuilder(behavior_name='fake',
            parameters={"alpha": 0.5})
        # knowledge builder needs to be saved to the DB first (its ID is needed
        # to store the graph)
        knowledge_builder.save()
        knowledge_builder.build_knowledge(self.topic)
        # retrieve the graph
        knowledge_graph = KnowledgeGraph.objects.all().first()
        self.assertIsNotNone(knowledge_graph)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)
        #print knowledge_graph


# ----------------------------------------------------------------------------
#  Behaviors Tests
# ----------------------------------------------------------------------------

# NOTE: nevim, jak tyhle testy delat, aby byla jistota, ze se nepouzivaji
# online zdroje a pritom hodnota techto testu je opravdu nizka, takze se bez
# nich zatim objedu
#class BehaviorsTestCase(TestCase):
#    def setUp(self):
#        self.BEHAVIORS = [
#            ('simple', {'alpha': 0.5})
#        ]
#        self.article = Article()
#        self.article = Article(self.article)

#    def test_behavior(self):
#        for behavior_name, parameters in self.BEHAVIORS:
#            knowledge_builder = KnowledgeBuilder(
#                behavior_name=behavior_name,
#                parameters=parameters)
#            behavior = knowledge_builder.get_behavior()
#            knowledge_graph = behavior.build_knowledge_graph(self.article)
#            self.assertIsInstance(knowledge_graph, KnowledgeGraph)


# ----------------------------------------------------------------------------
#  Global Knowledge Tests
# ----------------------------------------------------------------------------

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
