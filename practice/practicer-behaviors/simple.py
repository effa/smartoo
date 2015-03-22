from collections import defaultdict
from common.utils.metrics import cosine_similarity
#from exercises.models import Exercise
from practice import PracticerBehavior


class Simple(PracticerBehavior):
    """
    Simple practicer behavior
    -----------------------

    TODO: description (see comments below)
    NOTE: this model does not take into account the order of questions
    but since during one session the questions are relatively unique, we
    do not need to model learning, just the prior knowledge, so it is OK

    Parameters:
        'target-success': ideal overall ratio of correct answers
        'relevance-weight': relative weight of relevance vs. correctness
        'difficulty-weight': relative weight of difficulty vs. correctness
    """
    def next_exercise(self, graded_exercises, accumulated_feedback, feedbacked_exercises):
        # parameters
        target_success = self.get_parameter('target-success')
        relevance_weight = self.get_parameter('relevance-weight')
        difficulty_weight = self.get_parameter('difficulty-weight')
        repetitiveness_weight = self.get_parameter('repetitiveness_weight')

        correct_ratio = accumulated_feedback.get_correct_ratio()
        total_count = accumulated_feedback.get_all_answered_count()
        target_difficulty = compute_target_difficulty(target_success,
            correct_ratio, total_count)
        #print '---'
        #print 'target_difficulty:', target_difficulty

        # compute how many times each term was already used
        terms_history_counts = defaultdict(int)
        for feedbacked_exercise in feedbacked_exercises:
            for t1, t2 in feedbacked_exercise.exercise.get_term_pairs():
                terms_history_counts[t1] += 1
                terms_history_counts[t2] += 1

        def compute_history_similarity(graded_exercise):
            exercise_terms = graded_exercise.exercise.get_terms_counts()
            history_similarity = cosine_similarity(exercise_terms, terms_history_counts)
            return history_similarity

        def scoring_function(graded_exercise):
            repetitiveness_penalization = (-1) * compute_history_similarity(graded_exercise)
            difficulty_penalization = (-1) * abs(target_difficulty - graded_exercise.difficulty)
            score = graded_exercise.correctness\
                + relevance_weight * graded_exercise.relevance\
                + difficulty_weight * difficulty_penalization\
                + repetitiveness_weight * repetitiveness_penalization
            return score

        # find the exercise which maximizes the scoring function
        best_exercise = graded_exercises[0]
        best_score = 0
        for exercise in graded_exercises:
            score = scoring_function(exercise)
            #print exercise, score
            if score > best_score:
                best_exercise = exercise
                best_score = score

        return best_exercise


# ---------------------------------------------------------------------------
#  Helper functions
# ---------------------------------------------------------------------------

def compute_target_difficulty(target_success, correct_ratio, total_count):
    """
    Computes adjusted target difficulty, i.e. optimal difficulty of next
    exercise. Target difficulty is based on the desired :target_sucess:,
    but adjusted according to the actual success (if the user has higher
    actual success, we want to select more difficult question).
    """
    # correct ratio stabilization (make the recommendations at the
    # beginning less influened by the success rate)
    stabilizator_weight = 1.0 / (total_count + 1)
    actual_success = (1 - stabilizator_weight) * correct_ratio\
        + (stabilizator_weight * target_success)

    if actual_success >= target_success:
        slope = target_success / (1.0 - target_success)
        adjusted_target_success = slope * (1.0 - actual_success)
    else:
        slope = (1.0 - target_success) / target_success
        adjusted_target_success = 1.0 - slope * actual_success

    target_difficulty = 1 - adjusted_target_success
    return target_difficulty
