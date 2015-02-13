from common.utils.nlp import contextfree_sentences, join_words
from knowledge import KnowledgeBuilderBehavior
from knowledge.models import KnowledgeGraph
from knowledge.namespaces import SMARTOO, RDF, RDFS
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

        for sentence in contextfree_sentences(article):
            # TODO: tohle by chtelo delat spis pomoci reqexu/gramatiky
            before_term = []
            after_term = []
            term_found = False
            #print sentence
            #print '='
            for chunk in sentence:
                if not term_found:
                    if chunk.label() == 'TERM':
                        term_uri = chunk.uri
                        # !!! TODO: problem se sklonovanim, lepe pouzit global
                        # knowledge pro zijsteni labelu
                        term_text = join_words(chunk.leaves())
                        term_found = True
                        continue
                        # TODO: pomocna metoda na vytvoreni uri z pojmenovane
                        # entity (ve forme ParentedTree)
                    before_term.extend(chunk.leaves())
                else:
                    after_term.extend([token[0] for token in chunk.leaves()])

            if not term_found:
                continue

            # add quaisifact about a term in a sentence to the graph
            quasifact = BNode()
            knowledge_graph.add((
                quasifact,
                RDF['type'],
                Literal('term-in-sentence')))
            # parts
            knowledge_graph.add((
                quasifact,
                SMARTOO['term'],
                term_uri))
            knowledge_graph.add((
                quasifact,
                SMARTOO['part-before-term'],
                Literal(join_words(before_term))))
            knowledge_graph.add((
                quasifact,
                SMARTOO['part-after-term'],
                Literal(join_words(after_term))))
            # info about the term
            knowledge_graph.add((
                term_uri,
                RDF['type'],
                SMARTOO['term']))
            knowledge_graph.add((
                term_uri,
                RDFS['label'],
                Literal(term_text)))

        return knowledge_graph
