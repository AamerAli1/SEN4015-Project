from .models import Pin


import uuid
def updatePin():
     code = uuid.uuid4().hex[:4].upper()
     to_change = Pin.objects.get(id = 1)
     to_change.passcode = code
     to_change.save()
     print(code)

