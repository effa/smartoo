from __future__ import unicode_literals
from abstract_component import ComponentBehavior


class KnowledgeBuilderBehavior(ComponentBehavior):
    """
    Base class for all knowledge builder behaviors.
    """
    def build_knowledge_graph(self, article):
        """
        Creates knowledge graph for given topic.

        Args:
            article (knowledge.Article): article for whitch to build
                a knowledge graph
        Retuns:
            knowledge graph (knowledge.models.KnowledgeGraph)
        """
        raise NotImplementedError
