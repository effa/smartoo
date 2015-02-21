"""
Smartoo exceptions hieararchy
"""


class SmartooError(Exception):
    """
    Base class for all smartoo-specific exceptions.
    """
    pass


class SessionError(SmartooError):
    """
    Errors raised during a session step.
    """
    pass
