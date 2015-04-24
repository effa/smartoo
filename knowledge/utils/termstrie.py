from __future__ import unicode_literals
from nltk import word_tokenize, pos_tag


class TermsTrie(object):

    """Trie of terms of easy longest-matching term lookup

    TODO: blizsi popis pouziti

                    +-> square +-> END -> "blue squares"
        +-> blue ->|
        |          +-> triangle +-> END -> "blue triangles"
     +->|
        |           +-> END -> "white"
        +-> white ->|
                    +-> cube +-> END -> "white cubes"
    """

    _TERM_END = 0

    def __init__(self):
        self._trie = {}
        self._current = self._trie

    def add(self, name, tagged_name, rewrite=True):
        """Add new term to termtrie

        :name: [unicode] name of the term
        :tagged_name: list of tagged tokens
        """
        node = self._trie
        for token in tagged_name:
            # bylo by lepsi pouzivat lemmata misto slov
            # lowercase the token
            word = token[0].lower()
            # step down one level in trie; create empty subtrie
            # if it hasn't existed before
            node = node.setdefault(word, {})
        if rewrite or TermsTrie._TERM_END not in node:
            node[TermsTrie._TERM_END] = name

    def add_with_subnames(self, name, tagged_name=None):
        if tagged_name is None:
            tagged_name = pos_tag(word_tokenize(name))

        if not tagged_name:
            return

        # full name
        self.add(name, tagged_name, rewrite=True)

        # prefixes with at least one proper noun
        contains_proper_name = tagged_name[0][1] == 'NNP'
        for i in range(1, len(tagged_name) - 1):
            contains_proper_name = contains_proper_name or tagged_name[i][1] == 'NNP'
            if contains_proper_name:
                self.add(name, tagged_name[:i + 1], rewrite=False)

        # suffixes with at least one proper noun
        contains_proper_name = False
        for i in range(len(tagged_name) - 1, 0, -1):
            contains_proper_name = contains_proper_name or tagged_name[i][1] == 'NNP'
            if contains_proper_name:
                self.add(name, tagged_name[i:], rewrite=False)

    def get(self, canonical_form):
        """Returns term if there is one with given canonical form (else None)

        :canonical_form: [list<unicode>]
        """
        self.search_start()
        for lemma in canonical_form:
            possible_continuation = self.search_continue(lemma)
            if not possible_continuation:
                return None
        return self.search_result()

    def search_start(self, first_lemma=None):
        """Starts multistep search

        Continue by TermsTrie.search_continue...
        """
        self._current = self._trie
        if first_lemma is not None:
            return self.search_continue(first_lemma)

    def search_continue(self, lemma):
        """Continues with search by adding new lemma

        :return: True if given lemma was possible next step, False otherwise
        """
        if self._current is None:
            # TODO: specializovanejsi vyjimka?
            raise Exception('no search to continue in (use search_start())')
        lemma = lemma.lower()
        if lemma in self._current:
            self._current = self._current[lemma]
            return True
        else:
            self._current = None
            return False

    def search_result(self):
        """Returns current search results

        :return: term name if search was succesful, None otherwise
        """
        if self._current is None:
            return None
        # if there is the end of a term, return the term (None otherwise)
        return self._current.get(TermsTrie._TERM_END, None)
