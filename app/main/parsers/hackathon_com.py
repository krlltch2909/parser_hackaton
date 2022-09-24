from datetime import datetime
import os
import requests
from main.models import *


def get_hackathon_com_events():
    feeduid = os.environ.get("FEEDUID")
    response = requests.get(f"https://feeds.tildacdn.com/api/getfeed/?feeduid={feeduid}")
    data = response.json()

    events = []
    for raw_event in data["posts"]:
        event = Event()
        event.title = raw_event["title"]
        event.description = raw_event["descr"]
        event.registration_deadline = datetime.strptime(raw_event["date"], "%Y-%m-%d %H:%M") \
            .replace(tzinfo=None)

        if event.registration_deadline < datetime.now():
            continue

        event.url = raw_event["url"]
        event.img = raw_event["image"]
        event.status_of_event = StatusOfEvent.objects.get(status_code=4) # registration
        event.type_of_event = EventTypeClissifier.objects.get(type_code=2) # hackathon
        events.append(event)
    
    return events