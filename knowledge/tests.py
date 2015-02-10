# encoding=utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from knowledge import Article
from knowledge.models import KnowledgeBuilder, Vertical
from knowledge.models import KnowledgeGraph, GlobalKnowledge
from knowledge.namespaces import RESOURCE
#from knowledge.utils.sparql import prepared_query
from rdflib import Graph, Literal, Namespace
from unittest import skipIf

# flag: whether or not skip test which connects to online public endpoint
SKIP_ONLINE = True


class VerticalTestCase(TestCase):
    def setUp(self):
        Vertical.objects.create(
            topic_uri='http://en.wikipedia.org/wiki/Pan_Tau',
            content='test')

    def test_vertical_retrieval(self):
        vertical = Vertical.objects.get(
            topic_uri='http://en.wikipedia.org/wiki/Pan_Tau')
        self.assertIsNotNone(vertical)
        self.assertEqual(vertical.topic_uri,
            'http://en.wikipedia.org/wiki/Pan_Tau')
        self.assertEqual(vertical.get_name(), 'Pan Tau')

    def test_nonexisting_vrtical_retrieval(self):
        with self.assertRaises(ObjectDoesNotExist):
            Vertical.objects.get(
                topic_uri='http://en.wikipedia.org/wiki/Russell')

    def test_content_retrieval(self):
        vertical = Vertical.objects.get(
            topic_uri='http://en.wikipedia.org/wiki/Pan_Tau')
        self.assertEqual(vertical.content, 'test')


class KnowledgeGraphTestCase(TestCase):
    def setUp(self):
        # create topic_uri and knowledge builder
        self.topic_uri = 'http://en.wikipedia.org/wiki/Pan_Tau',
        self.knowledge_builder = KnowledgeBuilder.objects.create(
            behavior_name='fake', parameters={})

    def test_serialization_deserialization(self):
        # create knowledge graph and serialize it
        graph = Graph()
        NS = Namespace('http://example.com/test/')
        graph.bind('ns', NS)
        graph.add((NS['Tom'], NS['likes'], Literal('apples')))
        KnowledgeGraph.objects.create(
            knowledge_builder=self.knowledge_builder,
            topic_uri=self.topic_uri,
            graph=graph)
        # graph retrieval
        knowledge_graph = KnowledgeGraph.objects.all().first()
        graph2 = knowledge_graph.graph
        # check that the graph after serialization-deserialization is still the
        # same as it was
        self.assertTrue(graph2.isomorphic(graph))


class KnowledgeBuilderTestCase(TestCase):
    def setUp(self):
        self.topic_uri = 'http://en.wikipedia.org/wiki/Pan_Tau',
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
    def setUp(self):
        self.vertical = '''
<doc id="7" url="http://en.wikipedia.org/wiki/Abraham_Lincoln"\
     title="Abraham Lincoln">
<p heading="1">
<term wuri="Abraham_Lincoln">
Abraham	NP	Abraham-n
Lincoln	NP	Lincoln-n
</term>
</p>
<p>
<s>
<term wuri="Abraham_Lincoln" uncertainty="1">
Abraham	NP	Abraham-n
Lincoln	NP	Lincoln-n
</term>
was	VBD	be-v
the	DT	the-x
<term wuri="List_of_Presidents_of_the_United_States">
16	CD	16-x
<g/>
th	NN	th-n
president	NN	president-n
of	IN	of-i
the	DT	the-x
United	NP	United-n
States	NPS	States-n
</term>
<g/>
.	SENT	.-x
</s>
<s>
Lincoln	NP	Lincoln-n
led	VVD	lead-v
the	DT	the-x
United	NP	United-n
States	NPS	States-n
through	IN	through-i
its	PP$	its-d
<term wuri="American_Civil_War">
Civil	NP	Civil-n
War	NP	War-n
</term>
<g/>
.	SENT	.-x
</s>
'''.strip()

        self.article = Article(
            uri='http://en.wikipedia.org/wiki/Abraham_Lincoln',
            vertical=self.vertical)
        #self.maxDiff = None

    def test_get_vertical(self):
        self.assertEqual(self.article.get_name(), 'Abraham Lincoln')
        self.assertEqual(self.article.get_uri(), 'http://en.wikipedia.org/wiki/Abraham_Lincoln')
        self.assertEqual(len(self.article.get_sentences()), 2)


# ----------------------------------------------------------------------------
#  Behaviors Tests
# ----------------------------------------------------------------------------

class BehaviorsTestCase(TestCase):
    def setUp(self):
        self.BEHAVIORS = [
            ('simple', {'alpha': 0.5})
        ]
        self.vertical = 'test'
        self.article = Article(
            uri='http://en.wikipedia.org/wiki/Abraham_Lincoln',
            vertical=self.vertical)

    def test_behavior(self):
        for behavior_name, parameters in self.BEHAVIORS:
            knowledge_builder = KnowledgeBuilder(
                behavior_name=behavior_name,
                parameters=parameters)
            behavior = knowledge_builder.get_behavior()
            knowledge_graph = behavior.build_knowledge_graph(self.article)
            self.assertIsInstance(knowledge_graph, KnowledgeGraph)


# ----------------------------------------------------------------------------
#  Global Knowledge Tests
# ----------------------------------------------------------------------------

class GlobalKnowledgeTestCase(TestCase):
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

    #NOTE: query nebude GlobalKnowledge vubec implementovat
    #def test_query(self):
    #    query = prepared_query('''
    #        SELECT ?label
    #        WHERE {
    #            dbpedia:Henry_VIII_of_England: rdfs:label ?label
    #        }
    #        ''')
    #    result = self.global_knowledge.query(query)
    #    self.assertIsNotNone(result)
    #    self.assertEqual(len(result), 1)
    #    #print result.__dict__
    #    self.assertEqual(next(iter(result)), 'Henry VIII')
