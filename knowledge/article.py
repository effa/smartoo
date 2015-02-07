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

class Token(object):
    """
    Token representation
    """

    def __init__(self, line):
        """
        :line: [unicode] one line (one token) of vertical file
        """
        parts = line.split('\t')
        self._word = parts[0]
        # treetagger: 2nd column is tag, 3rd is lemma
        self._tag = parts[1] if len(parts) >= 2 else None
        self._lemma = parts[2] if len(parts) >= 3 else None

    def get_word(self):
        return self._word

    def get_tag(self):
        return self._tag

    def get_lemma(self):
        return self._lemma

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        """
        Returns unicode representation of the token (as one line)
        """
        return '{word}\t{tag}\t{lemma}'.format(
            word=self.get_word(),
            tag=self.get_tag(),
            lemma=self.get_lemma())


# -----------------------------------------------------------------------------
#  Article class
# -----------------------------------------------------------------------------


class Article(object):
    """
    Class for representation and extraction of data from one article.
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

        # building representation of vertical (store lines, tranform tokens to
        # Token objects)
        self._lines = []
        for line in lines:
            line = line.strip()
            # skip empty lines
            if not line:
                continue
            elif is_xml_tag(line):
                # if it's sgml tag, leave it as a string,
                self._lines.append(line)
            else:
                # use Token class to represent tokens
                token = Token(line)
                self._lines.append(token)

        # TODO: provide functionallity ... podle toho, co se zjisti, ze je
        # potreba

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '<Article name="{name}">'.format(name=self.get_name())

    def get(self, index):
        """Returns line (Token or sgml tag in unicode) on given index
        """
        return self._lines[index]

    def get_vertical(self, new_line=False):
        # NOTE: some lines are Tokens and some are strings
        vertical = '\n'.join(map(unicode, self._lines))
        if new_line:
            vertical += '\n'
        return vertical

    def get_uri(self):
        return self._uri

    def get_name(self):
        """
        Returns the name of the article.
        """
        return uri_to_name(self.get_uri())

    # TODO: inspirace z wikicorpora (vertical.py)
