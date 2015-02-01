class ComponentBehavior(object):
    """
    Base abstract class for component's behavior.
    """

    def __init__(self, parameters):
        """
        Args:
            parameters: dictionary of component parameters
        """
        self._parameters = parameters

    def get_parameter(self, parameter_name):
        return self._parameters[parameter_name]
