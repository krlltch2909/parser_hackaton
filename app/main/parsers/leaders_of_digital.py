import requests 
from datetime import datetime
from main.models import *
from .utils import get_event_status_based_on_date


def get_leaders_of_digital_events():
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get("https://leadersofdigital.ru/api/v1/site_get_all/0", headers=headers)
    data = response.json()
    raw_events = data["event"]
    events = []

    for raw_event in raw_events:
        event = Event()
        event.title = raw_event["name"]
        event.description = raw_event["description"]
        raw_event_start_date = raw_event["start_date"]
        event.start_date = datetime.fromisoformat(raw_event_start_date)
        raw_event_end_date = raw_event["end_date"]
        event.end_date = datetime.fromisoformat(raw_event_end_date)
        event.url = f'https://leadersofdigital.ru/event/{raw_event["event_id"]}'
        event.img = raw_event["avatar_big_url"]
        event.type_of_event = EventTypeClissifier.objects.get(type_code=2) # hackaton

        if raw_event['registration']:
            event.status_of_event = StatusOfEvent.objects.get(status_code=4) # registration
        else:
            event.status_of_event = get_event_status_based_on_date(event)
            
        events.append(event)

    return events
