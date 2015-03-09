from __future__ import unicode_literals
import nltk


# TODO: pravdepodobne potreba implementovat nejake vlastni regularni vyrazy nad
# Parented Tree

class RuleBasedRelationExtractor(object):

    def __init__(self, pattern=''):
        """
        Args:
            pattern: regular expression describing relation
        """
        grammar = r"""
        RELATION: {.* <NN>.*}
        """
        self.parser = nltk.RegexpParser(grammar, loop=2)

    def extract_relation(self, sentence):
        """
        Tries to find a relation given by :self.pattern: in a :sentence:

        Args:
            sentence: tree representation of a sentenced with named entities
        Returns:
            (subject, predicate, object) OR None
        """
        #tree = self.parser.parse(sentence)
        #print tree
        return None
