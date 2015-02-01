from __future__ import unicode_literals
from abstract_component import ComponentBehavior


class KnowledgeBuilderBehavior(ComponentBehavior):
    """
    Base class for all knowledge builder behaviors.
    """
    def build_knowledge_graph(self, topic):
        """
        Creates knowledge graph for given topic.

        Args:
            topic (knowledge.models.Topic): topic for which to build
                the knowledge graph
        Retuns:
            knowledge graph (knowledge.models.KnowledgeGraph)
        """
        raise NotImplementedError
