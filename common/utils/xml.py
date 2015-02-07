from __future__ import unicode_literals

"""
Module for XML related utilities
"""


def is_xml_tag(string):
    """
    Returns True if :string: is a (possibly unicode) string representing
    opening/closing tag.
    """
    if not isinstance(string, basestring):
        return False
    return string[0] == '<' and string[-1] == '>'
