from django.core.management.base import BaseCommand
#from django.core.management.base import BaseCommand, CommandError

## enable online access
#import common.settings
#common.settings.ONLINE_ENABLED = True

from knowledge.models import Article
from knowledge.utils.terms import name_to_term
#from json import dumps
#from common.settings import ONLINE_ENABLED


class Command(BaseCommand):
    args = '<article_name>'
    help = 'Retrieves article using Wikipedia API and process it'

    def handle(self, *args, **options):
        topic_name = args[0]
        topic = name_to_term(topic_name)
        Article(topic=topic).save()
        #article = Article(topic=topic)
        #article.get_content_from_wikipedia()
        #output = dumps(article.content)
        ##self.stdout.write(dumps(article.content))
        #with open('output.tmp', 'w') as f:
        #    f.write(output)
