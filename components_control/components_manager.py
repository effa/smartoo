#!/usr/bin/env python
# encoding: utf-8

from components_config import COMPONENT_TYPES
from common.paths import project_path
import imp


class ComponentsManager(object):
    """
    Class for components managment: registers new components and manages
    their data (code path, parameters, performance).
    """
    def get_component(self, component_id):
        # vyuzit self._get_component_behavior k zisakni definice chovani
        # komponenty, v __init__() se dasadi parametry (z DB)
        pass

    # TODO: preorganizovat (tato funkcionalita byla presunuta primo do
    # komponent)

    def _get_component_behavior(self, component_type, name):
        """
        Returns instantiated component behavior object.

        Args:
            component_type (unicode):
                allowed values are given by keys
                in components_config.COMPONENT_TYPES
            name (unicode):
                name under which is the component stored
        Returns:
            component behavior object (abstract_component.ComponentBehavior)
        Raises:
            ValueError: if the component_type is invalid
                        if there is no component behavior under given name
        """
        # retrieve info about this component type
        try:
            component_info = COMPONENT_TYPES[component_type]
        except KeyError:
            raise ValueError("Invalid component type: %s") % component_type

        # create full path of the behavior file
        behavior_path = project_path('{directory}{name}.py'.format(
            directory=component_info['behaviors-path'],
            name=name))

        # load the file with behavior
        # TODO: osetrit neexistenci zdroje
        behavior_module = imp.load_source('component_module', behavior_path)

        # instantiate the component behavior object
        class_name = component_info['behavior-class']
        behavior_object = getattr(behavior_module, class_name)
        return behavior_object


# TODO: pouzit Django prikazy pro management
#def main():
#    """
#    Command Line Interface for components managment
#    """
#    # demo:
#    c = ComponentsManager().getComponentBehavior('knowledge builder',
#        'fake')
#    print c
#    pass


#if __name__ == '__main__':
#    main()
