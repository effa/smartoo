from __future__ import unicode_literals
#from django.db import models
from abstract_component.models import Component


class Practicer(Component):
    """
    Model for practicer component.
    """

    def __unicode__(self):
        return '<Practicer {name}>'.format(name=self.name)
