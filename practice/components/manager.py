#!/usr/bin/env python
# encoding: utf-8

"""
Module for components managment.
Includes ComponentsManager class and CLI.
"""

import imp


class ComponentsManager(object):
    """
    Class for components managment: registers new components and manages
    their data (code path, parameters, performance).
    """
    # TODO ...
    pass


def main():
    """
    Command Line Interface for components managment
    """
    # demo instanciace komponenty
    PATH = '/home/tom/Documents/lab/smartoo/practice/components/knowledge-builders/knowledgebuilder.py'
    knowledge_builder_modul = imp.load_source('knowledgebuilder', PATH)
    knowledge_builder = knowledge_builder_modul.KnowledgeBuilder()
    knowledge_builder.build_knowledge_graph()





if __name__ == '__main__':
    main()
