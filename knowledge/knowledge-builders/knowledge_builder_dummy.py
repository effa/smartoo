from practice.components import Component


class KnowledgeBuilder(Component):

    def build_knowledge_graph(self, topic):
        """
        Pretends to create knowledge graph for given topic.

        Args:
            topic (???.Topic): topic for which to build the knowledge
        """
        pass  # do nothing

    def get_knowledge_graph(self):
        """
        Returns simple knowledge graph which has nothing to do with the topic.
        (It is just a demo...)

        Return:
            knowledge graph
        """
        raise NotImplementedError("interface method not implemented")
