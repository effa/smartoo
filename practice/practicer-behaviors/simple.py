from collections import defaultdict
from common.utils.metrics import cosine_similarity
#from exercises.models import Exercise
from practice import PracticerBehavior
from practice.utils.logistic_model import estimate_knowledge, correct_answer_probability
from practice.utils.target_probability_adjustment import compute_target_probability


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

    def next_exercise(self, unused_graded_exercises, accumulated_feedback,
            feedbacked_exercises):
        # parameters
        target_success = self.get_parameter('target-success')
        relevance_weight = self.get_parameter('relevance-weight')
        difficulty_weight = self.get_parameter('difficulty-weight')
        repetitiveness_weight = self.get_parameter('repetitiveness_weight')

        # compute adjusted target difficulty based on current correct ratio
        # and total number of answered questions
        correct_ratio = accumulated_feedback.get_correct_ratio()
        total_count = accumulated_feedback.get_all_answered_count()
        target_probability = compute_target_probability(target_success, correct_ratio, total_count)

        # create lists of exercises difficulties for exercises answered
        # correctly and incorrectly
        correct, incorrect = [], []
        for feedbacked_exercise in feedbacked_exercises:
            difficulty = feedbacked_exercise.exercise.difficulty
            if feedbacked_exercise.answered:
                if feedbacked_exercise.correct:
                    correct.append(difficulty)
                else:
                    incorrect.append(difficulty)

        # estimate knowledge using logistic model of student
        knowledge = estimate_knowledge(correct, incorrect)

        # compute how many times each term was already used
        terms_history_counts = defaultdict(int)
        for feedbacked_exercise in feedbacked_exercises:
            for t1, t2 in feedbacked_exercise.get_exercise().get_term_pairs():
                terms_history_counts[t1] += 1
                terms_history_counts[t2] += 1

        def compute_history_similarity(graded_exercise):
            exercise_terms = graded_exercise.exercise.get_terms_counts()
            history_similarity = cosine_similarity(exercise_terms, terms_history_counts)
            return history_similarity

        def scoring_function(graded_exercise):
            # difficulty score
            probability = correct_answer_probability(knowledge, graded_exercise.difficulty)
            difficulty_score = (-1) * abs(probability - target_probability)

            # relevance score
            relevance_score = graded_exercise.relevance

            # repetiveness score
            repetitiveness_score = (-1) * compute_history_similarity(graded_exercise)

            # total score
            score = graded_exercise.correctness\
                + relevance_weight * relevance_score\
                + difficulty_weight * difficulty_score\
                + repetitiveness_weight * repetitiveness_score
            return score

        # find the exercise which maximizes the scoring function
        best_exercise = unused_graded_exercises[0]
        best_score = float('-inf')
        for exercise in unused_graded_exercises:
            score = scoring_function(exercise)
            #print exercise, score
            if score > best_score:
                best_exercise = exercise
                best_score = score

        return best_exercise
