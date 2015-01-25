class KnowledgeBuilder(object):
    """
    Template (interface) for all knowledge builders
    """
    def build_knowledge_graph(topic, rebuild=True):
        """
        Creates and stores knowledge graph for given topic.

        Args:
            topic (???.Topic): topic for which to build the knowledge
            rebuild (bool): whether rebuild knowledge graph if already built
        """
        raise NotImplementedError("interface method not implemented")

    def get_knowledge_graph():
        """
        Returns built knowledge graph. Possibly the graph can be built only
        partially (in asynchronous setting) or even empty (if called before any
        knowledge building).
        """
        raise NotImplementedError("interface method not implemented")
