from components_control import ComponentsManager
from django.core.management.base import BaseCommand
#from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    #help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        c = ComponentsManager()._get_component_behavior('knowledge builder',
            'fake')
        self.stdout.write(str(c))
