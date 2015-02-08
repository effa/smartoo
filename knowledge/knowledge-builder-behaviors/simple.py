from common.utils.nlp import contextfree_sentences
from knowledge import KnowledgeBuilderBehavior
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import SMARTOO, RDFS
from rdflib import Literal, BNode


"""
Simple Knowledge Builder Behavior
-------------------------------

TODO: describe, possibly rename
Create (pseudo)facts about sentences with terms.
"""


class Simple(KnowledgeBuilderBehavior):

    def build_knowledge_graph(self, article):
        knowledge_graph = KnowledgeGraph()
        #for sentence in contextfree_sentences(article):
        #    # TODO: find a term, split in pre and post part
        #    terms_positions = sentence.get_terms_positions()
        #    if terms_positions:
        #        # only create one fact from one sentence
        #        # (take the last term)
        #        term_start, term_end = terms_positions[-1]
        #        term = sentence[term_start:term_end]
        #        preterm = sentence[:term_start]
        #        postterm = sentence[term_end:]
        #        quasifact = BNode()
        #        knowledge_graph.add((
        #            quasifact,
        #            RDFS['type'],  # or RDF?
        #            Literal('term-in-sentence')))
        #        knowledge_graph.add((
        #            quasifact,
        #            SMARTOO['part/term'],
        #            term))
        #        knowledge_graph.add((
        #            quasifact,
        #            SMARTOO['part/term'],
        #            term))
        #        knowledge_graph.add((
        #            quasifact,
        #            SMARTOO['part/preterm'],
        #            Literal(unicode(preterm))))
        #        knowledge_graph.add((
        #            quasifact,
        #            SMARTOO['part/postterm'],
        #            Literal(unicode(postterm))))
        return knowledge_graph
