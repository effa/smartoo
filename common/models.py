from django.db import models


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
    index = models.BigIntegerField()
