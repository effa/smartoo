from __future__ import division

from itertools import product
from collections import defaultdict
from random import uniform

from knowledge.models import KnowledgeBuilder
from exercises.models import ExercisesCreator, ExercisesGrader
from practice.models import Practicer
from smartoo.exceptions import SmartooError


class ComponentsSelector(object):
    """
    Class for intelligent selecting session components.
    """

    def __init__(self, session_manager):
        self._session_manager = session_manager

    def select_components(self):
        """
        Selects session components quadruple. The better performance
        had a component in the past, the more likely it will be chosen
        (using conditional probability).

        Returns:
            (knowledge.models.KnowledgeExtractor,
             exercises.models.ExerciseCreator,
             exercises.models.ExerciseGrader,
             practice.models.Practicer)
        Raises:
            django.core.exceptions.ObjectDoesNotExist: if there is no available
                componente for a step
        """
        knowledge_builders = KnowledgeBuilder.objects.filter(enabled=True)
        exercises_creators = ExercisesCreator.objects.filter(enabled=True)
        exercises_graders = ExercisesGrader.objects.filter(enabled=True)
        practicers = Practicer.objects.filter(enabled=True)

        components_lists = map(
            lambda queryset: queryset.values_list('pk', flat=True),
            [knowledge_builders, exercises_creators,
                exercises_graders, practicers])

        # check that there is at least one enabled component for each step
        if any([not queryset.exists() for queryset in components_lists]):
            raise SmartooError("No enabled components for a step.")

        #print knowledge_builders.values_list('id', flat=True)
        #print knowledge_builders.values_list('pk', flat=True)

        performances = self.create_performances_list(components_lists)

        # use bayes to randomly select components
        components_keys = []
        for step in range(4):
            component_key = weighted_choice(performances, step)
            components_keys.append(component_key)
            # filter performances
            performances = [p for p in performances if p[step] == component_key]

        knowledge_builder = knowledge_builders.get(pk=components_keys[0])
        exercises_creator = exercises_creators.get(pk=components_keys[1])
        exercises_grader = exercises_graders.get(pk=components_keys[2])
        practicer = practicers.get(pk=components_keys[3])

        return (knowledge_builder, exercises_creator,
                exercises_grader, practicer)

    # mozne dalsi metody (podle potreby): vyber jedine komponenty / podmnoziny
    # komponent, vyber zatim nejlepsich komponent

    def create_performances_list(self, components_lists):
        performances = defaultdict(list)

        # retrieve all sessions with their feedbacks
        # NOTE: sessions with small number of questions should be perioically
        # deleted
        sessions = self._session_manager.all()
        for session in sessions:
            components_keys = (
                session.knowledge_builder.pk,
                session.exercises_creator.pk,
                session.exercises_grader.pk,
                session.practicer.pk)
            performance = session.feedback.get_performance()
            performances[components_keys].append(performance)

        # smoothing: add one made up session with average performance
        AVERAGE_PERFORMANCE = 0.5
        for components_keys in product(*components_lists):
            performances[tuple(components_keys)].append(AVERAGE_PERFORMANCE)

        # transform to list and shrink to average number for a components-combo
        performances_list = []
        for components_keys in performances:
            component_performances = performances[components_keys]
            performance = sum(component_performances) / len(component_performances)
            performance_record = list(components_keys)
            performance_record.append(performance)
            performances_list.append(performance_record)

        return performances_list


# ----------------------------------------------------------
#  Helper functions
# ----------------------------------------------------------

def weighted_choice(performances, step):
    total = sum(p[-1] for p in performances)
    random_point = uniform(0, total)
    current_point = 0
    for performance in performances:
        weight = performance[-1]
        if current_point + weight >= random_point:
            return performance[step]
        current_point += weight
    # for sure
    return performances[-1][step]
