"""
Simple text processing utilities..
"""


def capitalize_first_letter(string):
    """
    Same as capitalize() but leaves the other letter untouched.

    E.g.: 'abCd Efg' -> 'AbDd Efg'
    """
    if string:
        string = string[0].upper() + string[1:]
    return string
