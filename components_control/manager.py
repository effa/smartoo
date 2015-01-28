#!/usr/bin/env python
# encoding: utf-8

"""
Module for components managment.
Includes ComponentsManager class and CLI.
"""

from components import COMPONENT
import imp


class ComponentsManager(object):
    """
    Class for components managment: registers new components and manages
    their data (code path, parameters, performance).
    """

    def getComponentByName(self, component_type, name):
        """
        Returns instantiated component.

        Args:
            component_type (practice.components.components.COMPONENT).
            name (unicode): name under with is the component stored.
        Returns:
            instantiated component
        Raises:
            ValueError: if the component_type is invalid
                        if there is no component under given name
        """
        # zasadni TODO: predat komponentam jejich parametry (v initu)
        # demo: vraci dummy komponenty
        BASE = '/home/tom/Documents/lab/smartoo/..........'
        if component_type == COMPONENT.KNOWLEDGE_BUILDER:
            file_path = BASE + 'knowledge-builders/knowledge_builder_dummy.py'
            knowledge_builder_module = imp.load_source('kb_module', file_path)
            return knowledge_builder_module.KnowledgeBuilder()
        elif component_type == COMPONENT.EXERCISES_CREATOR:
            file_path = BASE + 'exercises-creators/exercises_creator_dummy.py'
            exercises_creator_module = imp.load_source('ec_module', file_path)
            return exercises_creator_module.ExercisesCreator()
        elif component_type == COMPONENT.EXERCISES_GRADER:
            file_path = BASE + 'exercises-grader/exercises_grader_dummy.py'
            exercises_grader_module = imp.load_source('ed_module', file_path)
            return exercises_grader_module.ExercisesGrader()
        elif component_type == COMPONENT.PRACTICER:
            file_path = BASE + 'practicers/practicer_dummy.py'
            practicer_module = imp.load_source('practicer_module', file_path)
            return practicer_module.Practicer()
        else:
            raise ValueError("Invalid component type: %s" % component_type)


def main():
    """
    Command Line Interface for components managment
    """
    pass


if __name__ == '__main__':
    main()
