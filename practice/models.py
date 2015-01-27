from django.db import models


# ---------------------------------------------------------------------------
#  Components
# ---------------------------------------------------------------------------

class KnowledgeBuilder(models.Model):
    code_path = models.CharField(max_length=200)  # max length ?
    performance = models.DecimalField(max_digits=10, decimal_places=10)


class KnowledgeBuilderParameter(models.Model):
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    key = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=10)


# TODO: dalsi komponenty podobne


# ---------------------------------------------------------------------------
#   Session
# ---------------------------------------------------------------------------

class Session(models.Model):
    # topic
    # ??? topic = models.ForeignKey(Term) ???

    # components
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    # atd ...

    # feedback
    correct_count = models.SmallIntegerField(default=0)
    wrong_count = models.SmallIntegerField(default=0)
    unanswered_count = models.SmallIntegerField(default=0)
    invalid_count = models.SmallIntegerField(default=0)
    # + details (later) ...

    def select_components(self):
        # TODO: select components
        pass

    def get_new_exercise(self):
        """
        Returns new exercise or None if the practice session is over.
        It can take a while to return a new exercise (they have to be
        generated and graded and this is not instant).

        Returns:
            new exercise (Exercise)
        """
        # demo exercise TODO: trida Exercise, metoda to_dictionary
        exercise = {
            'question': 'When was George Washington born?',
            'options': ['1732', '1782', '1890', '1921']}
        return exercise

    def provide_feedback(self, feedback):
        """
        Notifies the manager about user answer to the last question.

        Args:
            feedback (Feedback): user's feedback (includes the answer)
        """
        pass


# ---------------------------------------------------------------------------
#   ??? Data
# ---------------------------------------------------------------------------

# TODO: Term a Knowledge ???

class Exercise(models.Model):
    question = models.TextField()
    knowledge_builder = models.ForeignKey(KnowledgeBuilder)
    #exercises_creator = models.ForeignKey(ExercisesCreator)
    # possibly: image, map, type (multichoice/free answer/...), ...


class Options(models.Model):
        exercise = models.ForeignKey(Exercise)
        correct = models.BooleanField(default=True)
        string = models.CharField(max_length=500)  # possibly declined etc.
        # + reference na term do Knowledge (potreba semantickych informaci
        #   kvuli ohodnoceni otazky


class ExerciseGrade(models.Model):
    exercise = models.ForeignKey(Exercise)
    #exercise_grader = models.ForeignKey(ExerciseGrader)
