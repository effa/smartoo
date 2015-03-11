#from exercises.models import Exercise
from practice import PracticerBehavior


class Simple(PracticerBehavior):
    """
    Simple practicer behavior
    -----------------------

    TODO: description
    """
    def next_exercise(self, graded_exercises, accumulated_feedback):
        # TODO: prizpusobovat obtiznost, na kterou mireme, podle feedbacku
        target_difficulty = 0.5

        # TODO: vazey prumer (parametry komponenty)
        def scoring_function(graded_exercise):
            difficulty_penalization = (-1) * abs(target_difficulty - graded_exercise.difficulty)
            return graded_exercise.correctness + graded_exercise.relevance + difficulty_penalization

        # nalezeni cviceni maximulizujici skorovaci funkci
        best_exercise = graded_exercises[0]
        best_score = 0
        for exercise in graded_exercises:
            score = scoring_function(exercise)
            if score > best_score:
                best_exercise = exercise
                best_score = score

        return best_exercise
