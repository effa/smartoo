from __future__ import unicode_literals


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

    def add(self, name, canonical_form):
        """Add new term to termtrie

        :name: [unicode] name of the term
        :canonical_form: [list<unicode>] list of tokens
        """
        node = self._trie
        for lemma in canonical_form:
            # step down one level in trie; create empty subtrie
            # if it hasn't existed before
            node = node.setdefault(lemma, {})
        # TODO: hlasit problem 2 kanonickych forem s ruznymy nazvy
        node[TermsTrie._TERM_END] = name

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
