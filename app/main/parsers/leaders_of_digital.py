import requests 
from datetime import datetime
from main.models import *


def get_leaders_of_digital_events():
    response = requests.get("https://leadersofdigital.ru/api/v1/site_get_all/0")
    data = response.json()
    raw_events = data["event"]
    events = []

    for raw_event in raw_events:
        event = Event()

        if "registration_deadline_date" not in raw_event.keys():
            continue
        
        event.title = raw_event["name"]
        event.description = raw_event["description"]
        event.registration_deadline = datetime.fromisoformat(raw_event["registration_deadline_date"]) \
            .replace(tzinfo=None)

        if event.registration_deadline < datetime.now():
            continue

        event.url = f'https://leadersofdigital.ru/event/{raw_event["event_id"]}'
        event.img = raw_event["avatar_big_url"]
        event.type_of_event = EventTypeClissifier.objects.get(type_code=2) # hackathon
        event.status_of_event = StatusOfEvent.objects.get(status_code=4) # registration
        events.append(event)

    return events
