# TODO: obalit KnowledgeBuilder (vzdy) objektem pro spravu persistence (bude
# ukladat vytvoreny graf, umoznovat neopakovat vypocet pro jiz vytvoreny graf,
# ziskat graf z DB.
from practice.components import Component


class KnowledgeBuilder(Component):
    """
    Template for all knowledge builders
    """
    def build_knowledge_graph(self, topic):
        """
        Creates knowledge graph for given topic.

        Args:
            topic (???.Topic): topic for which to build the knowledge
        """
        raise NotImplementedError("interface method not implemented")

    def get_knowledge_graph(self):
        """
        Returns built knowledge graph. Possibly the graph can be built only
        partially (in asynchronous setting) or even empty (if called before any
        knowledge building).

        Return:
            knowledge graph
        """
        raise NotImplementedError("interface method not implemented")
