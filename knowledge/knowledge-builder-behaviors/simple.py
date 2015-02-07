from common.utils.nlp import contextfree_sentences
from knowledge import KnowledgeBuilderBehavior
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import SMARTOO, RDFS
from rdflib import Literal, BNode


"""
Simple Knowledge Builder Behavior
-------------------------------

TODO: describe, possibly rename
Create facts of
"""


class Simple(KnowledgeBuilderBehavior):

    def build_knowledge_graph(self, article):
        knowledge_graph = KnowledgeGraph()
        for sentence in contextfree_sentences(article):
            # TODO: find a term, split in pre and post part
            term = 'todo'
            preterm = 'todo'
            postterm = 'todo'
            quasifact = BNode()
            knowledge_graph.add((
                quasifact,
                RDFS['type'],  # or RDF?
                Literal('term-in-sentence')))
            knowledge_graph.add((
                quasifact,
                SMARTOO['term'],
                term))
            knowledge_graph.add((
                quasifact,
                SMARTOO['preterm'],
                Literal(preterm)))
            knowledge_graph.add((
                quasifact,
                SMARTOO['postterm'],
                Literal(postterm)))
        return knowledge_graph
