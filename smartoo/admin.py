from django.contrib import admin
from knowledge.models import Vertical, KnowledgeBuilder
from exercises.models import Exercise, GradedExercise
from exercises.models import ExercisesCreator, ExercisesGrader

# models admin registration
admin.site.register(Vertical)
admin.site.register(KnowledgeBuilder)
admin.site.register(Exercise)
admin.site.register(GradedExercise)
admin.site.register(ExercisesCreator)
admin.site.register(ExercisesGrader)
