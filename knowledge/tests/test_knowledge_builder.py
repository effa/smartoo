# encoding=utf-8

from __future__ import unicode_literals
from django.test import TestCase
from knowledge.models import KnowledgeBuilder, Article
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import TERM


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
