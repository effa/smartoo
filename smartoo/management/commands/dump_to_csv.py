from __future__ import unicode_literals
from django.core.management.base import BaseCommand
#from django.core.management.base import BaseCommand, CommandError
from smartoo.models import Session
from knowledge.utils.terms import term_to_name


class Command(BaseCommand):
    args = '<file_name>'
    help = 'Dumps data to csv'

    def handle(self, *args, **options):
        if len(args) > 0:
            file_name = args[0]
        else:
            file_name = 'data.csv'
        self.stdout.write('Dumping data to ' + file_name)
        with open(file_name, 'w') as f:
            format_description = '{sid};{kb};{ec};{eg};{pr}'\
                + ';{correct};{wrong};{unanswered};{invalid};{irrelevant}'\
                + ';{final_rating:.1f};{performance:.5f}'\
                + ';{topic}'
            f.write('#' + format_description + '\n')
            for session in Session.objects.all():
                feedback = session.feedback
                line = format_description.format(
                    sid=session.pk,
                    topic=term_to_name(session.topic),
                    kb=session.knowledge_builder.pk,
                    ec=session.exercises_creator.pk,
                    eg=session.exercises_grader.pk,
                    pr=session.practicer.pk,
                    correct=feedback.correct_count,
                    wrong=feedback.wrong_count,
                    unanswered=feedback.unanswered_count,
                    invalid=feedback.invalid_count,
                    irrelevant=feedback.irrelevant_count,
                    final_rating=feedback.final_rating,
                    performance=feedback.get_performance()
                )
                f.write((line + '\n').encode('utf-8'))
