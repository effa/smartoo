from collections import defaultdict
from common.utils.metrics import cosine_similarity_exercise_article
from knowledge.models import Article
from exercises import ExercisesGraderBehavior
from exercises.models import GradedExercise
from exercises.utils.difficulty import normalized_average_similarity


class Simple(ExercisesGraderBehavior):
    """
    Simple Exercises Grader Behavior
    ------------------------------

    Description: Uses heuristics to rank relevance and difficulty.
    Parameters: no parameters
    """
    def setup(self, topic):
        self.article = Article.objects.get(topic=unicode(topic))

    def grade_exercise(self, exercise):
        knowledge_graph = exercise.knowledge_graph
        #topic = knowledge_graph.topic

        similarities = []
        terms = defaultdict(int)

        for t1, t2 in exercise.get_term_pairs():
            similarities.append(knowledge_graph.similarity(t1, t2))
            terms[t1] += 1
            terms[t2] += 1

        # set difficulty to normalized average_similarity
        difficulty = normalized_average_similarity(similarities)

        # Relevance is based on the frequence of terms in the article.
        # All terms are used, not just the correct answer (because we want to
        # penalize questions with irrelevant distractors), but to give more
        # weight on the correct answer (in multiple-choice questions) we will
        # count each occurence in term_pairs. (Note that this approach is not
        # limited to multiple choice questions.)

        # Relevance is set as a cosine similiarity between article and the
        # exercise (only terms counted).
        relevance = cosine_similarity_exercise_article(terms, self.article)

        correctness = 0.5

        return GradedExercise(
            difficulty=difficulty,
            correctness=correctness,
            relevance=relevance)
