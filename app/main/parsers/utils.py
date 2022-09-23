from datetime import datetime
from main.models import *


def get_event_status_based_on_date(event):
    if event.start_date > datetime.now() and event.end_date < datetime.now():
        return StatusOfEvent.objects.get(status_code=1) # in process
    elif event.start_date > datetime.now():
        return StatusOfEvent.objects.get(status_code=3) # unavailable
    else:
        return StatusOfEvent.objects.get(status_code=2) # ended