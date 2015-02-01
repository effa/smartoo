from __future__ import unicode_literals
from django.db import models
from common.fields import DictField
from common.paths import project_path, to_camel_case
import imp


class Component(models.Model):
    """
    Abstract super class for all components.
    Each component is composed of behavior (code) and parameters.
    """
    # name of the behavior (same as the name of the behavior (code) file)
    behavior = models.CharField(max_length=50)
    # parameters: json dict
    parameters = DictField()

    # NOTE: We store parameters in json (dictionary), because it's more
    # flexible than relational table of parameters and we don't need fast
    # single parameter lookup.

    class Meta:
        abstract = True

    @classmethod
    def get_behaviors_path(cls):
        raise NotImplementedError

    def get_behavior(self):
        """
        Returns instantiated component behavior initalized with parameters.
        """
        # create full path of the behavior file
        behavior_path = project_path('{directory}{name}.py'.format(
            directory=self.get_behaviors_path(),
            name=self.behavior))

        # load the file with behavior
        # TODO: osetrit neexistenci zdroje
        behavior_module = imp.load_source('component_module', behavior_path)
        behavior_class_name = to_camel_case(self.behavior)

        # instantiate the component behavior object
        behavior_class = getattr(behavior_module, behavior_class_name)
        behavior_object = behavior_class(self.parameters)
        return behavior_object
