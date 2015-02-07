from __future__ import unicode_literals
from common.utils.wiki import uri_to_name

# NOTE: ? Presunout do models baliku ?


class Article(object):
    """
    Class for representation and extraction of data from one article.
    """

    def __init__(self, topic_uri, vertical):
        """
        Args:
            vertical: string representing the vertical of this article
        """
        self._topic_uri = topic_uri
        # TODO: process vertical

    def __unicode__(self):
        return '<Article name="{name}">'.format(topic=self.get_name())

    def get_name(self):
        """
        Returns the name of the article.
        """
        return uri_to_name(self.uri)

    # TODO: inspirace z wikicorpora (vertical.py)
