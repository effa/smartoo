from __future__ import unicode_literals
from django.db import models


class Component(models.Model):
    """
    Abstract super class for all components.
    Each component is composed of behavior (code) and parameters.
    """
    # name of the component (same as the name of the behavior (code) file)
    name = models.CharField(max_length=50)
    # parameters: json dict
    parameters = models.TextField()

    # NOTE: We sotre parameters in json (dictionary), because it's more
    # flexible than relational table of parameters and we don't need fast
    # single parameter lookup.

    class Meta:
        abstract = True
