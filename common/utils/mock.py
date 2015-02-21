"""
Module for simple mocking
"""

from __future__ import unicode_literals


class MockObject(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __unicode__(self):
        return '<MockObject {content}>'.format(content=self.__dict__)

    def __str__(self):
        return unicode(self).encode('utf-8')
