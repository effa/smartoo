from knowledge import KnowledgeBuilderBehavior
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import RESOURCE, ONTOLOGY, RDFS, DC, XSD
from rdflib import Literal


"""
Fake Knowledge Builder Behavior
-------------------------------

Creates a simple knowledge graph without looking at the topic.
"""


class Fake(KnowledgeBuilderBehavior):

    def build_knowledge_graph(self, topic):
        knowledge_graph = KnowledgeGraph(topic=topic)
        henry = RESOURCE['Henry_VIII_of_England']
        knowledge_graph.add((henry,
            RDFS['label'],
            Literal('Henry VIII of England')))
        knowledge_graph.add((henry,
            DC['description'],
            Literal('King of England')))
        knowledge_graph.add((henry,
            ONTOLOGY['birthDate'],
            Literal('1491-06-28', datatype=XSD.date)))
        return knowledge_graph
