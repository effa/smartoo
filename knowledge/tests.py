# encoding=utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from knowledge import Article
from knowledge.models import KnowledgeBuilder, Vertical, Topic, KnowledgeGraph
from rdflib import Graph, Literal, Namespace


class TopicTestCase(TestCase):
    def setUp(self):
        vertical = Vertical.objects.create(content='test')
        Topic.objects.create(
            uri='http://en.wikipedia.org/wiki/Pan_Tau',
            vertical=vertical)

    def test_topic_retrieval(self):
        topic = Topic.objects.get(uri='http://en.wikipedia.org/wiki/Pan_Tau')
        self.assertIsNotNone(topic)
        self.assertEqual(topic.uri, 'http://en.wikipedia.org/wiki/Pan_Tau')
        self.assertEqual(topic.get_name(), 'Pan Tau')

    def test_nonexisting_topic_retrieval(self):
        with self.assertRaises(ObjectDoesNotExist):
            Topic.objects.get(uri='http://en.wikipedia.org/wiki/Russell')

    def test_retrieving_vertical_for_topic(self):
        topic = Topic.objects.get(uri='http://en.wikipedia.org/wiki/Pan_Tau')
        vertical = topic.vertical
        self.assertEqual(vertical.content, 'test')


class KnowledgeGraphTestCase(TestCase):
    def setUp(self):
        # create vertical, topic and knowledge builder
        self.vertical = Vertical.objects.create(
            content='test')
        self.topic = Topic.objects.create(
            uri='http://en.wikipedia.org/wiki/Pan_Tau',
            vertical=self.vertical)
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
            topic=self.topic,
            graph=graph)
        # graph retrieval
        knowledge_graph = KnowledgeGraph.objects.all().first()
        graph2 = knowledge_graph.graph
        # check that the graph after serialization-deserialization is still the
        # same as it was
        self.assertTrue(graph2.isomorphic(graph))


class KnowledgeBuilderTestCase(TestCase):
    def setUp(self):
        # create a vertical and a topic
        self.vertical = Vertical.objects.create(
            content='test')
        self.topic = Topic.objects.create(
            uri='http://en.wikipedia.org/wiki/Pan_Tau',
            vertical=self.vertical)

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
        self.maxDiff = None

    def test_get_vertical(self):
        pass
        #self.assertMultiLineEqual(self.article.get_vertical(), self.vertical)


# ----------------------------------------------------------------------------
#  Behaviors Tests
#  ---------------
#  These should be independent of the DB layer. (But we will still use
#  Knowledge Builder class a little bit since it has some functionality we need
#  (instantiation of behavior instance))
#  TODO: tohle nejsou klasicke unit testy, chtelo by to nejak oddelit
# ----------------------------------------------------------------------------

class BehaviorsTestCase(TestCase):
    def setUp(self):
        self.BEHAVIORS = [
            ('simple', {'alpha': 0.5})
        ]
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

    def test_behavior(self):
        for behavior_name, parameters in self.BEHAVIORS:
            knowledge_builder = KnowledgeBuilder(
                behavior_name=behavior_name,
                parameters=parameters)
            behavior = knowledge_builder.get_behavior()
            knowledge_graph = behavior.build_knowledge_graph(self.article)
            self.assertIsInstance(knowledge_graph, KnowledgeGraph)
            # see the outputted knowledge graph
            #print '*' * 70
            #print 'Behavior name:', behavior_name, '| parameters:', parameters
            #print '*' * 70
            #print knowledge_graph
            #print '*' * 70
