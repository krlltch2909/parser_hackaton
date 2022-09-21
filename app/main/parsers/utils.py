from datetime import datetime
from main.models import *


def get_event_status_based_on_date(event):
    if event.start_date > datetime.now() and event.end_date < datetime.now():
        return StatusOfEvent.objects.get(id=1) # in process
    elif event.start_date > datetime.now():
        return StatusOfEvent.objects.get(id=3) # unavailable
    else:
        return StatusOfEvent.objects.get(id=2) # ended