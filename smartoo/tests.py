from django.test import TestCase
from knowledge.models import Article, KnowledgeGraph, KnowledgeBuilder
from knowledge.namespaces import TERM
from exercises.models import Exercise, ExercisesCreator
from exercises.models import GradedExercise, ExercisesGrader
from practice.models import Practicer
from smartoo.models import Session, AccumulativeFeedback, FeedbackedExercise
from smartoo.exceptions import SmartooError


class AccumulativeFeedbackTestCase(TestCase):
    def setUp(self):
        pass

    def test_default(self):
        #feedback = AccumulativeFeedback.objects.create_empty_feedback()
        feedback = AccumulativeFeedback.objects.create()
        self.assertIsInstance(feedback, AccumulativeFeedback)
        self.assertEqual(feedback.correct_count, 0)
        self.assertEqual(feedback.wrong_count, 0)
        self.assertEqual(feedback.unanswered_count, 0)
        self.assertEqual(feedback.invalid_count, 0)
        self.assertEqual(feedback.irrelevant_count, 0)
        # retrieve the feedback from DB to test it was saved
        feedback = AccumulativeFeedback.objects.get(pk=feedback.pk)
        # and repeat the same tests again for this retrieved feedback
        self.assertIsInstance(feedback, AccumulativeFeedback)
        self.assertEqual(feedback.correct_count, 0)
        self.assertEqual(feedback.wrong_count, 0)
        self.assertEqual(feedback.unanswered_count, 0)
        self.assertEqual(feedback.invalid_count, 0)
        self.assertEqual(feedback.irrelevant_count, 0)

    def test_add(self):
        #feedback = AccumulativeFeedback.objects.create_empty_feedback()
        feedback = AccumulativeFeedback.objects.create()
        feedback.add(FeedbackedExercise(
            answered=True,
            correct=False,
            invalid=False,
            irrelevant=True))
        self.assertEqual(feedback.correct_count, 0)
        self.assertEqual(feedback.wrong_count, 1)
        self.assertEqual(feedback.unanswered_count, 0)
        self.assertEqual(feedback.invalid_count, 0)
        self.assertEqual(feedback.irrelevant_count, 1)
        feedback.add(FeedbackedExercise(
            answered=False,
            correct=False,
            invalid=True,
            irrelevant=False))
        self.assertEqual(feedback.correct_count, 0)
        self.assertEqual(feedback.wrong_count, 1)
        self.assertEqual(feedback.unanswered_count, 1)
        self.assertEqual(feedback.invalid_count, 1)
        self.assertEqual(feedback.irrelevant_count, 1)

    def test_get_calculated_counts(self):
        feedback = AccumulativeFeedback.objects.create()
        self.assertEqual(feedback.get_all_answered_count(), 0)
        self.assertEqual(feedback.get_all_questions_count(), 0)
        self.assertEqual(feedback.get_good_questions_count(), 0)
        self.assertAlmostEqual(feedback.get_correct_ratio(), 0.5)

        feedback.add(FeedbackedExercise(
            answered=True,
            correct=True,
            invalid=False,
            irrelevant=True))

        self.assertEqual(feedback.get_all_answered_count(), 1)
        self.assertEqual(feedback.get_all_questions_count(), 1)
        self.assertEqual(feedback.get_good_questions_count(), 0)
        self.assertAlmostEqual(feedback.get_correct_ratio(), 1.0)

        feedback.add(FeedbackedExercise(
            answered=True,
            correct=False,
            invalid=False,
            irrelevant=False))

        self.assertEqual(feedback.get_all_answered_count(), 2)
        self.assertEqual(feedback.get_all_questions_count(), 2)
        self.assertEqual(feedback.get_good_questions_count(), 1)
        self.assertAlmostEqual(feedback.get_correct_ratio(), 0.5)

        feedback.add(FeedbackedExercise(
            answered=False,
            correct=False,
            invalid=False,
            irrelevant=True))

        self.assertEqual(feedback.get_all_answered_count(), 2)
        self.assertEqual(feedback.get_all_questions_count(), 3)
        self.assertEqual(feedback.get_good_questions_count(), 1)
        self.assertAlmostEqual(feedback.get_correct_ratio(), 0.5)

    def test_get_performance(self):
        feedback = AccumulativeFeedback.objects.create()
        self.assertAlmostEqual(feedback.get_performance(), 0.5)

        feedback.add(FeedbackedExercise(
            answered=False,
            correct=False,
            invalid=False,
            irrelevant=True))

        self.assertAlmostEqual(feedback.get_performance(), 2.5 / 6)

        feedback.add(FeedbackedExercise(
            answered=True,
            correct=False,
            invalid=False,
            irrelevant=False))

        self.assertAlmostEqual(feedback.get_performance(), 3.5 / 7)

        feedback.final_rating = 1.0
        self.assertAlmostEqual(feedback.get_performance(), 6.0 / 7)

        feedback.final_rating = 0.0
        self.assertAlmostEqual(feedback.get_performance(), 1.0 / 7)


class SessionTestCase(TestCase):
    def setUp(self):
        # create topic uri and article
        self.topic = TERM['Pan_Tau']
        Article.objects.create(
            topic=self.topic,
            content=Article.EMPTY_CONTENT)
        # create fake components in the DB
        KnowledgeBuilder.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})
        ExercisesCreator.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})
        ExercisesGrader.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})
        Practicer.objects.create(
            behavior_name='fake',
            parameters={"alpha": 1.0})

    def test_create_session(self):
        session = Session.objects.create_with_components(self.topic)
        self.assertIsNotNone(session)
        self.assertEqual(session.topic, self.topic)
        self.assertIsInstance(session.knowledge_builder, KnowledgeBuilder)
        self.assertIsInstance(session.exercises_creator, ExercisesCreator)
        self.assertIsInstance(session.exercises_grader, ExercisesGrader)
        self.assertIsInstance(session.practicer, Practicer)
        self.assertEqual(session.finnished, False)

    def test_select_components(self):
        # test that session do not select disabled component
        ExercisesGrader.objects.all().update(enabled=False)
        with self.assertRaises(SmartooError):
            Session.objects.create_with_components(self.topic)

    def test_build_knowledge(self):
        session = Session.objects.create_with_components(self.topic)
        session.build_knowledge()
        knowledge_graph = KnowledgeGraph.objects.all().first()
        self.assertIsNotNone(knowledge_graph)
        self.assertIsInstance(knowledge_graph, KnowledgeGraph)

    def test_create_graded_exercises(self):
        session = Session.objects.create_with_components(self.topic)
        # TODO: lepsi by bylo tam graf vlozit manualne (abychom se zbavili
        # zavislosti na uspechu build_knowledge()
        session.build_knowledge()
        session.create_graded_exercises()
        exercises = Exercise.objects.all()
        grades = GradedExercise.objects.all()
        # check that exercises and grades were stored
        self.assertGreater(len(exercises), 0,
            "No exercises were stored.")
        self.assertGreater(len(grades), 0,
            "No grades were stored.")
        self.assertEqual(len(exercises), len(grades),
            "The number of stored grades and exercises is different.")

    def test_get_graded_exercises(self):
        session = Session.objects.create_with_components(self.topic)
        session.build_knowledge()
        session.create_graded_exercises()
        exercises = session.get_graded_exercises()
        self.assertGreater(len(exercises), 0)
        self.assertIsInstance(exercises[0], GradedExercise)

    def test_next_exercise(self):
        session = Session.objects.create_with_components(self.topic)
        session.build_knowledge()
        session.create_graded_exercises()
        exercise = session.next_exercise()
        # should return Exercise, not GradedExercise
        self.assertIsInstance(exercise, Exercise)

    def test_provide_feedback(self):
        """
        Test that after n calls of provide_feedback, there will be n used
        exericises and (all - n) unused exercises.
        """
        session = Session.objects.create_with_components(self.topic)
        session.build_knowledge()
        session.create_graded_exercises()
        # n-times new_exercises -> feedback
        all_exercises = len(session.get_graded_exercises())
        for i in range(all_exercises):
            # check the counts of used vs. unused exercises
            used = len(session.get_feedbacked_exercises())
            unused = len(session.get_unused_graded_exercises())
            self.assertEqual(used, i)
            self.assertEqual(unused, all_exercises - i)
            # get and provide feedback for next exercise
            exercise = session.next_exercise()
            feedback = {
                'pk': exercise.pk,
                'answered': True,
                'correct': True,
                'invalid': False,
                'irrelevant': False}
            session.provide_feedback(feedback)
        # all exercises used, the next one should be None
        self.assertIsNone(session.next_exercise())
