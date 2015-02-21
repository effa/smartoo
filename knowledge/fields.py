from django.db import models
from rdflib import Graph, URIRef
from common.utils.wiki import uri_to_name
from knowledge.namespaces import TERM

# we will use turtle syntax for RDF serialization, it is quite compact and
# readable (it is a subset of n3 (notatation3) and corresponds to SPARQL)
RDF_SERIALIZATION_FORMAT = 'turtle'


class GraphField(models.TextField):
    """
    Model field for rdflib.Graph
    """

    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, Graph):
            return value

        if value == '':
            return None

        # deserialize string
        graph = Graph()
        graph.parse(data=value, format=RDF_SERIALIZATION_FORMAT)
        return graph

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == '':
            return None

        if isinstance(value, Graph):
            value = value.serialize(format=RDF_SERIALIZATION_FORMAT)

        return super(GraphField, self).get_db_prep_save(value, *args, **kwargs)

    # serialization (e.g. for creating DB dumps in XML)
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        #return self.get_prep_value(value)
        return value.serialize(format=RDF_SERIALIZATION_FORMAT)


class TermField(models.CharField):
    """
    Model field for terms.
    All terms has the same namespace (knowledge.namespaces.RESOURCE), so we
    will store it wihout namespace
    """

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super(TermField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(TermField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, URIRef):
            return value
        if value == '' or value is None:
            return None
        # deserialize string
        # sometimes, value will be unicode with TERM prefix
        if value.startswith(TERM):
            term = URIRef(value)
        else:
            term = TERM[value.replace(' ', '_')]
        return term

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == '':
            return None
        if isinstance(value, URIRef):
            value = uri_to_name(value)
        return super(TermField, self).get_db_prep_save(value, *args, **kwargs)

    # serialization (e.g. for creating DB dumps in XML)
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        #return self.get_prep_value(value)
        #return unicode(value)
        return uri_to_name(value)
