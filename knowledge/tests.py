# encoding=utf-8

from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from knowledge import Article
from knowledge.models import KnowledgeBuilder, Vertical
from knowledge.models import KnowledgeGraph, GlobalKnowledge
from knowledge.namespaces import RESOURCE, RDF, RDFS, ONTOLOGY, SMARTOO
#from knowledge.utils.sparql import prepared_query
from rdflib import Graph, Literal, Namespace
from unittest import skipIf

# flag: whether or not skip test which connects to online public endpoint
SKIP_ONLINE = True

#TODO: rozdelit do vice souboru (podbalik pro testy)


class VerticalTestCase(TestCase):
    def setUp(self):
        Vertical.objects.create(
            topic_uri='http://dbpedia.org/resource/Pan_Tau',
            content='test')

    def test_vertical_retrieval(self):
        vertical = Vertical.objects.get(
            topic_uri='http://dbpedia.org/resource/Pan_Tau')
        self.assertIsNotNone(vertical)
        self.assertEqual(vertical.topic_uri,
            'http://dbpedia.org/resource/Pan_Tau')
        self.assertEqual(vertical.get_name(), 'Pan Tau')

    def test_nonexisting_vrtical_retrieval(self):
        with self.assertRaises(ObjectDoesNotExist):
            Vertical.objects.get(
                topic_uri='http://dbpedia.org/resource/Russell')

    def test_content_retrieval(self):
        vertical = Vertical.objects.get(
            topic_uri='http://dbpedia.org/resource/Pan_Tau')
        self.assertEqual(vertical.content, 'test')


class KnowledgeGraphTestCase(TestCase):
    #fixtures = ['knowledge-graph-henry8.xml', 'complete-lincoln.xml']
    fixtures = ['complete-lincoln.xml']

    def setUp(self):
        # get fake knowledge builder (already in DB: see fixture)
        self.knowledge_builder = KnowledgeBuilder.objects.get(
            behavior_name='fake', parameters={})

    def test_serialization_deserialization(self):
        # create knowledge graph and serialize it
        graph = Graph()
        NS = Namespace('http://example.com/test/')
        graph.bind('ns', NS)
        topic_uri = NS['Tom']
        graph.add((topic_uri, NS['likes'], Literal('apples')))
        KnowledgeGraph.objects.create(
            knowledge_builder=self.knowledge_builder,
            topic_uri=topic_uri,
            graph=graph)
        # graph retrieval
        knowledge_graph = KnowledgeGraph.objects.get(
            topic_uri=topic_uri)
        graph2 = knowledge_graph.graph
        # check that the graph after serialization-deserialization is still the
        # same as it was
        self.assertTrue(graph2.isomorphic(graph))

    def test_label(self):
        knowledge_graph = KnowledgeGraph()
        tomE = RESOURCE['Tom_E']
        tomF = RESOURCE['Tom_F']
        knowledge_graph.add((tomE, RDFS['label'], Literal('Tom')))
        self.assertEqual(knowledge_graph.label(tomE), 'Tom')
        self.assertEqual(knowledge_graph.label(tomF), 'Tom F')
        self.assertIsNone(knowledge_graph.label(tomF, fallback_guess=False))

    def test_types_of_term(self):
        term = RESOURCE['Abraham_Lincoln']
        knowledge_graph = KnowledgeGraph.objects.get(topic_uri=term)
        self.assertIsInstance(knowledge_graph.types_of_term, dict)
        self.assertIn(term, knowledge_graph.types_of_term)

    def test_terms_of_type(self):
        term = RESOURCE['Abraham_Lincoln']
        knowledge_graph = KnowledgeGraph.objects.get(topic_uri=term)
        self.assertIsInstance(knowledge_graph.terms_of_type, dict)
        self.assertIn(ONTOLOGY['Person'], knowledge_graph.terms_of_type)
        self.assertIn(term,
            knowledge_graph.terms_of_type[ONTOLOGY['Person']])

    def test_types(self):
        term = RESOURCE['Abraham_Lincoln']
        knowledge_graph = KnowledgeGraph.objects.get(
            topic_uri=term)
        types = knowledge_graph.types(term)
        self.assertIsInstance(types, set)
        self.assertIn(ONTOLOGY['Agent'], types)
        self.assertIn(ONTOLOGY['Person'], types)
        #self.assertIn(ONTOLOGY['Royalty'], types)
        #self.assertIn(ONTOLOGY['BritishRoyalty'], types)
        self.assertNotIn(ONTOLOGY['Activity'], types)

    def test_types_set_manually(self):
        knowledge_graph = KnowledgeGraph()
        termA = RESOURCE['A']
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        types = knowledge_graph.types(termA)
        self.assertIn(SMARTOO['term'], types)
        self.assertNotIn(ONTOLOGY['Activity'], types)

    def test_terms_similarity(self):
        knowledge_graph = KnowledgeGraph()
        termA = RESOURCE['A']
        termB = RESOURCE['B']
        # adding types and checking similarity after each step
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0)
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0)
        knowledge_graph.add((termB, RDF['type'], SMARTOO['term']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.5)
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Agent']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.5)
        knowledge_graph.add((termB, RDF['type'], ONTOLOGY['Person']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 0.5)
        knowledge_graph.add((termB, RDF['type'], ONTOLOGY['Agent']))
        self.assertAlmostEqual(knowledge_graph.similarity(termA, termB), 2.0 / 3)

    def test_all_terms(self):
        knowledge_graph = KnowledgeGraph()
        termA = RESOURCE['A']
        termB = RESOURCE['B']
        self.assertEqual(len(knowledge_graph.all_terms), 0)
        knowledge_graph.add((termA, RDF['type'], SMARTOO['term']))
        self.assertEqual(len(knowledge_graph.all_terms), 1)
        knowledge_graph.add((termA, RDF['type'], ONTOLOGY['Agent']))
        self.assertEqual(len(knowledge_graph.all_terms), 1)
        knowledge_graph.add((termB, RDF['type'], SMARTOO['term']))
        self.assertEqual(len(knowledge_graph.all_terms), 2)

    def test_get_all_resources(self):
        knowledge_graph = KnowledgeGraph()
        termA = RESOURCE['A']
        termB = RESOURCE['B']
        self.assertEqual(len(knowledge_graph.get_all_resources()), 0)
        knowledge_graph.add((termA, SMARTOO['sth'], SMARTOO['sth']))
        self.assertEqual(len(knowledge_graph.get_all_resources()), 1)
        knowledge_graph.add((SMARTOO['sth'], SMARTOO['sth'], termA))
        self.assertEqual(len(knowledge_graph.get_all_resources()), 1)
        knowledge_graph.add((SMARTOO['sth'], SMARTOO['sth'], termB))
        self.assertEqual(len(knowledge_graph.get_all_resources()), 2)
        self.assertIn(termA, knowledge_graph.get_all_resources())
        self.assertIn(termB, knowledge_graph.get_all_resources())

    def test_add_related_global_knowledge(self):
        # !!!!!!!!!!!!!!!!!!!!1
        # TODO: az to rozbehnu, vytvorit ze ziskanych dat fixtures
        # (complete-lincoln.xml) a zakazat pristup k online zdrojum
        topic = RESOURCE['Abraham_Lincoln']
        vertical = Vertical.objects.get(topic_uri=topic)
        article = Article(vertical=vertical)
        knowledge_graph = KnowledgeGraph(topic_uri=topic)
        knowledge_graph.add_related_global_knowledge(article, online=False)
        #print knowledge_graph
        #self.assertEqual(len(knowledge_graph.graph), 774)
        # there are 29 terms in article + Lincoln graph
        self.assertEqual(len(set(knowledge_graph.get_subjects())), 29)
        # test few triples in the graph
        self.assertIn(ONTOLOGY['Person'],
            knowledge_graph.types(RESOURCE['Abraham_Lincoln']))
        self.assertIn(ONTOLOGY['Person'],
            knowledge_graph.types(RESOURCE['Andrew_Johnson']))
        self.assertEqual(
            knowledge_graph.label(RESOURCE['Tad_Lincoln'], fallback_guess=False),
            'Tad Lincoln')


class KnowledgeBuilderTestCase(TestCase):
    def setUp(self):
        self.topic_uri = 'http://dbpedia.org/resource/Pan_Tau',
        Vertical.objects.create(
            topic_uri=self.topic_uri,
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
        knowledge_builder.build_knowledge(self.topic_uri)
        # retrieve the graph
        knowledge_graph = KnowledgeGraph.objects.all().first()
        self.assertIsNotNone(knowledge_graph)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)
        #print knowledge_graph


# ----------------------------------------------------------------------------
#  Article Tests
# ----------------------------------------------------------------------------

class ArticleTestCase(TestCase):
    fixtures = ['vertical-lincoln.xml']

    def setUp(self):
        self.topic_uri = 'http://dbpedia.org/resource/Abraham_Lincoln'
        self.vertical = Vertical.objects.get(topic_uri=self.topic_uri)
        self.article = Article(vertical=self.vertical)
        #self.maxDiff = None

    def test_parsing_vertical(self):
        self.assertEqual(self.article.get_name(), 'Abraham Lincoln')
        self.assertEqual(self.article.get_topic_uri(), self.topic_uri)
        self.assertEqual(len(self.article.get_sentences()), 2)

    def test_get_all_terms(self):
        terms = self.article.get_all_terms()
        self.assertIn(RESOURCE['Abraham_Lincoln'], terms)
        self.assertIn(RESOURCE['American_Civil_War'], terms)


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
#        self.vertical = Vertical()
#        self.article = Article(self.vertical)

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

    @skipIf(SKIP_ONLINE, 'connection to DBpedia public endpoint')
    def test_get_graph(self):
        term = RESOURCE['Henry_VIII_of_England']
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
    fixtures = ['global-knowledge.xml']

    def setUp(self):
        self.global_knowledge = GlobalKnowledge()

    def test_get_global_knowledge_builder(self):
        self.assertIsNotNone(self.global_knowledge.knowledge_builder)
        self.assertIsInstance(self.global_knowledge.knowledge_builder, KnowledgeBuilder)

    def test_get_graph(self):
        term = RESOURCE['Henry_VIII_of_England']
        knowledge_graph = self.global_knowledge.get_graph(term, online=False)
        self.assertIsNotNone(knowledge_graph)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)
        self.assertGreater(len(knowledge_graph.graph), 0)
        #print knowledge_graph
        #print 'number of triples:', len(knowledge_graph.graph)

    def test_label(self):
        henry = RESOURCE['Henry_VIII_of_England']
        label = self.global_knowledge.label(henry, fallback_guess=False)
        self.assertEqual(label, 'Henry VIII of England')

    #    self.assertEqual(next(iter(result)), 'Henry VIII')
