from knowledge import KnowledgeBuilderBehavior


"""
Fake Knowledge Builder Behavior
-------------------------------

Creates a simple knowledge graph without looking at the topic.
"""


class Fake(KnowledgeBuilderBehavior):

    def build_knowledge_graph(self, topic):
        pass
