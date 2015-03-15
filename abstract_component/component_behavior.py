class ComponentBehavior(object):
    """
    Base abstract class for component's behavior.
    """

    def __init__(self, parameters):
        """
        Args:
            parameters: dictionary of component parameters
        """
        if  parameters:
            self._parameters = parameters
        else:
            self._parameters = {}

    def get_parameter(self, parameter_name):
        return self._parameters[parameter_name]
