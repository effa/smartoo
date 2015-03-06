from django.contrib import admin
from knowledge.models import Article, KnowledgeBuilder, KnowledgeGraph
from exercises.models import Exercise, GradedExercise
from exercises.models import ExercisesCreator, ExercisesGrader
from practice.models import Practicer
from smartoo.models import FeedbackedExercise, Session, AccumulativeFeedback

# models admin registration
admin.site.register(Article)
admin.site.register(KnowledgeBuilder)
admin.site.register(KnowledgeGraph)
admin.site.register(Exercise)
admin.site.register(GradedExercise)
admin.site.register(ExercisesCreator)
admin.site.register(ExercisesGrader)
admin.site.register(Practicer)
admin.site.register(FeedbackedExercise)
admin.site.register(Session)
admin.site.register(AccumulativeFeedback)
