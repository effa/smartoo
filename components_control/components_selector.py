#from django.core.exceptions import ObjectDoesNotExist
from knowledge.models import KnowledgeBuilder
from exercises.models import ExercisesCreator, ExercisesGrader
from practice.models import Practicer


class ComponentsSelector(object):
    """
    Class for intelligent selecting session components.
    """

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
        # NOTE: zatim vracime "nahodne" komponenty
        knowledge_builder = KnowledgeBuilder.objects.all()[:1].get()
        exercises_creator = ExercisesCreator.objects.all()[:1].get()
        exercises_grader = ExercisesGrader.objects.all()[:1].get()
        practicer = Practicer.objects.all()[:1].get()
        return (knowledge_builder, exercises_creator,
                exercises_grader, practicer)

    # mozne dalsi metody (podle potreby): vyber jedine komponenty / podmnoziny
    # komponent, vyber zatim nejlepsich komponent
