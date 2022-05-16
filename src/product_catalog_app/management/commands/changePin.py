from django.core.management.base import BaseCommand, CommandError
from management.models import Pin

import uuid

class Command(BaseCommand):
    help = 'Generate a random pin Number'




    def handle(self, *args, **options):

        code = uuid.uuid4().hex[:4].upper()
        to_change = Pin.objects.get(id = 1)
        to_change.passcode = code
        to_change.save()
        


        self.stdout.write(self.style.SUCCESS('Successfully changed pin "%s"' % code))