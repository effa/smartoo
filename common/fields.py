from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json

"""
Custom model fields.
"""

# TODO: DictField - projit, okomentovat, otestovat, odladit


class DictField(models.TextField):
    """
    Field for dictionary, using JSON for storig in DB (in a text field).
    """

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return super(DictField, self).get_db_prep_save(value, *args, **kwargs)
