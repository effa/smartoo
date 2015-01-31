from django.db import models
from common.utils.wiki import uri_to_name


class Topic(models.Model):
    """
    Model for topics, which can be practiced. Corresponds to the articles
    on the Enlglish Wikipedia.
    """
    # URI of the term (resource) to practice
    # (same as the URL of the corresponding article)
    uri = models.CharField(max_length=120, unique=True)

    # index (start line) of the article in the vertical file
    # (vertical file of English Wikipedia with terms inferred)
    #index = models.BigIntegerField()
    # NOTE: index neni potreba, vertikal bude ulozen primo v DB jako
    # dlouhy string

    def get_name(self):
        """
        Returns the name of the topic.
        """
        return uri_to_name(self.uri)
