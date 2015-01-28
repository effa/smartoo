# This is basically simple configuration file to store information about all
# component types.
from collections import OrderedDict

COMPONENT_TYPES = OrderedDict([
    ('knowledge builder', {
        'model-path': 'knowledge/models.py',
        'model-class': 'KnowledgeBuilder',
        'behaviors-path': 'knowledge/knowledge-builder-behaviors/',
        'behavior-class': 'KnowledgeBuilderBehavior'
    })
    # TODO: ostatni komponenty


])

#COMPONENT_TYPES = component_info.keys()

#class ComponentType(object):
#    """
#    Enum class for components.
#    """
#    KNOWLEDGE_BUILDER = "knowledge builders"
#    EXERCISES_CREATOR = "exercises creators"
#    EXERCISES_GRADER = "exercises graders"
#    PRACTICER = "practicers"
