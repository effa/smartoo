"""
Utilities related to topic
"""
from knowledge.models import Vertical


def is_valid_topic(term):
    """
    Returns True if the term is a valid topic (= we have vertical for it)
    """
    return Vertical.objects.filter(topic=term).exists()
