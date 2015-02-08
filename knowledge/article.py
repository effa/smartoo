from __future__ import unicode_literals
from common.utils.xml import is_xml_tag
from common.utils.wiki import uri_to_name
import re

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

    def __init__(self, uri, vertical):
        """
        Args:
            vertical: string representing the vertical of this article,
                in tree-tagger format
        """
        self._uri = uri
        # assert top_uri == uri stated in the vertical header
        # (may remove topic_uri argument later, but for now, it's usefull
        # check, that we do things right)
        # TODO: process vertical
        # check :vertical: is unicode
        assert isinstance(vertical, basestring)
        vertical = unicode(vertical)
        lines = vertical.split('\n')

        # TODO: struktury (terms, math, ...) ??
        self._sentences = []
        new_sentence = []
        discard_sentence = False
        for line in lines:
            line = line.strip()
            # skip empty lines
            if not line:
                continue
            elif is_xml_tag(line):
                # if it's sgml tag, leave it as a string,
                term_match = TERM_TAG.match(line)
                if term_match:
                    # TODO
                    pass
                elif line == '</term>':
                    # TODO
                    pass
                elif line == '<s>':
                    new_sentence = []
                    discard_sentence = False
                elif line == '<g/>':
                    # ignore glue, we don't need it
                    pass
                elif line == '</s>':
                    print 'sentence'
                    print new_sentence
                    if not discard_sentence:
                        self._sentences.append(new_sentence)
                else:
                    # structure which is not handled (like <math>)
                    # -> discard the sentence
                    discard_sentence = True
            else:
                # use Token class to represent tokens
                #token = Token(line)
                #self._lines.append(token)
                token = line.split('\t')
                new_sentence.append(token)

        # TODO: provide functionallity ... podle toho, co se zjisti, ze je
        # potreba

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<Article name="{name}">'.format(name=self.get_name())

    #def get(self, index):
    #    """Returns line (Token or sgml tag in unicode) on given index
    #    """
    #    return self._lines[index]

    #def get_vertical(self, new_line=False):
    #    # NOTE: some lines are Tokens and some are strings
    #    vertical = '\n'.join(map(unicode, self._lines))
    #    if new_line:
    #        vertical += '\n'
    #    return vertical

    def get_uri(self):
        return self._uri

    def get_name(self):
        """
        Returns the name of the article.
        """
        return uri_to_name(self.get_uri())

    def get_sentences(self):
        """
        Returns list of sentences in the article.
        """
        return self._sentences
