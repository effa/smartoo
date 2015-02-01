from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from knowledge.models import KnowledgeBuilder, Vertical, Topic


class TopicTestCase(TestCase):

    def setUp(self):
        vertical = Vertical.objects.create(content='test line')
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
        self.assertEqual(vertical.content, 'test line')


class KnowledgeBuilderTestCase(TestCase):

    def test_create_two_builders_with_same_name(self):
        try:
            KnowledgeBuilder.objects.create(
                behavior='fake',
                parameters={"alpha": 0.5})
            KnowledgeBuilder.objects.create(
                behavior='fake',
                parameters={"alpha": 1.0})
        except:
            self.fail('Creating two components with the same behavior should'
                + ' be possible')

    def test_retrieval(self):
        # store knowledge builder to DB
        knowledge_builder = KnowledgeBuilder.objects.create(
            behavior='fake',
            parameters={"alpha": 0.5})
        key = knowledge_builder.pk
        # and check if everything is OK after retrieval
        knowledge_builder = KnowledgeBuilder.objects.get(pk=key)
        self.assertEqual(knowledge_builder.behavior, 'fake')
        self.assertEqual(knowledge_builder.parameters, {"alpha": 0.5})

    def test_behavior_instance(self):
        knowledge_builder = KnowledgeBuilder(behavior='fake',
            parameters={"alpha": 0.5})
        behavior = knowledge_builder.get_behavior()
        self.assertEqual(behavior.build_knowledge_graph(None), None)
        self.assertAlmostEqual(behavior.get_parameter('alpha'), 0.5)


#class KnowledgeGraphTextCase(TestCase):
#    kkk
