from management.models import Pin
from django.contrib.sessions.models import Session;

import uuid
def hi():
     Session.objects.all().delete()

     code = uuid.uuid4().hex[:4].upper()
     to_change = Pin.objects.get(id = 1)
     to_change.passcode = code
     to_change.save()
     print(code)
