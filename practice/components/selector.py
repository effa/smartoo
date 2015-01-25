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
            (KnowledgeExtractor, ExerciseCreator, ExerciseGrader, Practicer)
        Raises:
            MissingComponentException: if there is no available component for
                at least one session step.
        """
        pass

    # mozne dalsi metody (podle potreby): vyber jedine komponenty / podmnoziny
    # komponent, vyber zatim nejlepsich komponent
