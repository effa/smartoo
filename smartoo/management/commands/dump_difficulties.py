from __future__ import unicode_literals
from django.core.management.base import BaseCommand
#from django.core.management.base import BaseCommand, CommandError
from smartoo.models import FeedbackedExercise


class Command(BaseCommand):
    args = '<file_name>'
    help = 'Dumps question difficulties with ok/nok info to a file'

    def handle(self, *args, **options):
        if len(args) > 0:
            file_name = args[0]
        else:
            file_name = 'difficulties.csv'
        self.stdout.write('Dumping difficulties data to ' + file_name)
        with open(file_name, 'w') as f:
            format_description = '{difficulty};{correct}'
            f.write('#' + format_description + '\n')
            for feedbackedExercise in FeedbackedExercise.objects.all():
                if not feedbackedExercise.answered:
                    continue

                feedbackedExercise.exercise.difficulty
                feedbackedExercise

                line = format_description.format(
                    difficulty=feedbackedExercise.exercise.difficulty,
                    correct=int(feedbackedExercise.correct)
                )
                f.write((line + '\n').encode('utf-8'))
