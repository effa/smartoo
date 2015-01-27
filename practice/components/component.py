"""
Module for things related to components.
"""


class COMPONENT(object):
    """
    Enum class for components.
    """
    KNOWLEDGE_BUILDER = "knowledge builders"
    EXERCISES_CREATOR = "exercises creators"
    EXERCISES_GRADER = "exercises graders"
    PRACTICER = "practicers"


class Component(object):
    """
    Base class for all components
    """

    def __init__(self, parameters):
        """
        Args:
            parameters: dictionary of component parameters
        """
        self._parameters = parameters

    def get_parameter(self, parameter_name):
        return self._parameters(parameter_name)
