from __future__ import unicode_literals

from nltk import ParentedTree
from collections import defaultdict
import re

from common.utils.xml import is_xml_tag
from common.utils.wiki import uri_to_name
#from knowledge.models import Vertical
from knowledge.namespaces import RESOURCE

# NOTE: ? Presunout do models baliku ?

# -----------------------------------------------------------------------------
#  regular expressions
# -----------------------------------------------------------------------------

# regex matching a term sgml tag
TERM_TAG = re.compile(r"""
        ^
        <term
        \s+
        wuri="(?P<wuri>.*?)"
        .*
        >
        $
        """, re.VERBOSE)


# -----------------------------------------------------------------------------
#  Token class
# -----------------------------------------------------------------------------

#class Token(object):
#    """
#    Token representation
#    """

#    def __init__(self, line):
#        """
#        :line: [unicode] one line (one token) of vertical file
#        """
#        parts = line.split('\t')
#        self._word = parts[0]
#        # treetagger: 2nd column is tag, 3rd is lemma
#        self._tag = parts[1] if len(parts) >= 2 else None
#        self._lemma = parts[2] if len(parts) >= 3 else None

#    def get_word(self):
#        return self._word

#    def get_tag(self):
#        return self._tag

#    def get_lemma(self):
#        return self._lemma

#    def __str__(self):
#        return unicode(self).encode('utf-8')

#    def __unicode__(self):
#        """
#        Returns unicode representation of the token (as one line)
#        """
#        return '{word}\t{tag}\t{lemma}'.format(
#            word=self.get_word(),
#            tag=self.get_tag(),
#            lemma=self.get_lemma())


# -----------------------------------------------------------------------------
#  Article class
# -----------------------------------------------------------------------------


class Article(object):
    """
    Class for representation and extraction of data from one article.

    An article is represented as a list of sentences,
    each sentence is represented as a tree (nltk.Tree),
    where internal nodes are chunks (e.g. named entities)
    and leaves are tokens, stored as a tuple (word, pos-tag).

    Example:

    [
    Tree('S', [
        Tree({'type': 'PERSON',
            'uri': URIRef('http://dbpedia.org/resource/Abraham_Lincoln')},
            [('Abraham', 'NNP'), ('Lincoln', 'NNP')]),
        ('(', 'NNP'),
        Tree({'type': 'DATE',
              'literal': Literal('1809-02-12',datatype=XSD.date)},
            [('February', 'NNP'), ('12', 'CD'), (',', ','), ('1809', 'CD')]),
        ('-', ':'),
        Tree({'type': 'DATE',
              'literal': Literal('1865-04-15',datatype=XSD.date)},
            [('April', 'NNP'), ('15', 'CD'), (',', ','), ('1865', 'CD')]),
        (')', ':'),
        ('was', 'VBD'),
        Tree('TERM', [('the', 'DT'), ('16th', 'JJ'), ('President', 'NNP'),
                    ('of', 'IN'), ('the', 'DT'),
                    Tree('GPE', [('United', 'NNP'), ('States', 'NNPS')])]),
        ('.', '.')
    ]),
    # ... another sentences ...
    ]
])
    """

    def __init__(self, vertical):
        """
        Args:
            vertical: vertical from which to build the article
                [knowledge.models.Vertical]
        """
        self._topic_uri = vertical.topic_uri
        lines = vertical.content.split('\n')

        # _terms dictionary maps uri to list of references to positions (nodes)
        self._terms = defaultdict(list)
        self._sentences = []
        discarding = True
        for line in lines:
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            # if discarding, skip everything except for <s>
            if discarding and line != '<s>':
                continue

            if is_xml_tag(line):
                if line == '<s>':
                    new_sentence = ParentedTree('S', [])
                    discarding = False
                    current_node = new_sentence
                    continue

                term_match = TERM_TAG.match(line)
                if term_match:
                    # NOTE: it's easier to work with string labels than with
                    # dictionaries as a node (unfortunatelly)
                    wuri = term_match.group('wuri')
                    # TODO: use DBpedia to get more specific type sequence, e.g
                    # "TERM:AGENT:PERSON", "TERM:EVENT", "DATE", "NUMBER", ...
                    current_node = ParentedTree('TERM', [])
                    # save the uri information to the node
                    current_node.term = RESOURCE[wuri]
                    # remember term and its position
                    self._terms[current_node.term].append(current_node)

                elif line == '</term>':
                    new_sentence.append(current_node)
                    # change refference of current node back to the sentence
                    current_node = new_sentence

                elif line == '<g/>':
                    # ignore glue, we don't need it
                    pass

                elif line == '</s>':
                    #print 'sentence'
                    #print new_sentence
                    if not discarding:
                        self._sentences.append(new_sentence)

                else:
                    # structure which is not handled (like <math>)
                    # -> discard the sentence
                    discarding = True

            else:
                # use tuples to represent tokens
                #token = Token(line)
                #self._lines.append(token)
                token = tuple(line.split('\t'))
                pos_tag = token[1]
                current_node.append(ParentedTree(pos_tag, [token]))

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<Article name="{name}">'.format(name=self.get_name())

    #def get_vertical(self, new_line=False):
    #    # NOTE: some lines are Tokens and some are strings
    #    vertical = '\n'.join(map(unicode, self._lines))
    #    if new_line:
    #        vertical += '\n'
    #    return vertical

    def get_topic_uri(self):
        return self._topic_uri

    def get_name(self):
        """
        Returns the name of the article.
        """
        return uri_to_name(self.get_topic_uri())

    def get_all_terms(self):
        """
        Returns set of all terms in the article.
        """
        return set(self._terms.keys())

    def get_sentences(self):
        """
        Returns list of sentences in the article.
        """
        return self._sentences
