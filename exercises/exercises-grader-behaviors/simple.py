from collections import defaultdict
from common.utils.metrics import cosine_similarity_exercise_article
from knowledge.models import Article
from exercises import ExercisesGraderBehavior
from exercises.models import GradedExercise


class Simple(ExercisesGraderBehavior):
    """
    Simple Exercises Grader Behavior
    ------------------------------

    TODO: description
    Parameters: ---
    """
    def setup(self, topic):
        self.article = Article.objects.get(topic=topic.encode('utf-8'))

    def grade_exercise(self, exercise):
        knowledge_graph = exercise.knowledge_graph
        #topic = knowledge_graph.topic

        similarities = []
        terms = defaultdict(int)

        for t1, t2 in exercise.get_term_pairs():
            similarities.append(knowledge_graph.similarity(t1, t2))
            terms[t1] += 1
            terms[t2] += 1

        # set difficulty to average_similarity
        average_similarity = sum(similarities) / len(similarities)
        difficulty = average_similarity

        # Relevance is based on the frequence of terms in the article.
        # All terms are used, not just the correct answer (because we want to
        # penalize questions with irrelevant distractors), but to give more
        # weight on the correct answer (in multiple-choice questions) we will
        # count each occurence in term_pairs. (Note that this approach is not
        # limited to multiple choice questions.)

        # Relevance is set as a cosine similiarity between article and the
        # exercise (only terms counted).
        relevance = cosine_similarity_exercise_article(terms, self.article)

        # TODO: Extremely simple heuristic for correctness, such as length of
        # the exercise (cim delsi, tim vetsi pravdepodobnost problemu)
        correctness = 0.5

        return GradedExercise(
            difficulty=difficulty,
            correctness=correctness,
            relevance=relevance)
