from django.db import models
from rdflib import Graph

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
