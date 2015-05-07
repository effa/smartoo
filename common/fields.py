from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json

"""
Custom model fields.
"""


class DictField(models.TextField):
    """
    Field for dictionary, using JSON for storing in DB (in a text field).
    """

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        #print 'to python'
        #print type(value)
        #print value[:200]

        if value == "":
            return None

        if isinstance(value, dict):
            return value

        try:
            if isinstance(value, basestring):
                dictionary = json.loads(value)
                return dictionary
        except ValueError:
            pass

        return value

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return super(DictField, self).get_db_prep_save(value, *args, **kwargs)

    # serialization (e.g. for creating DB dumps in XML)
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return json.dumps(value)
