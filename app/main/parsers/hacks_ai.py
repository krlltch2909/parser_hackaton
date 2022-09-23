import requests
from datetime import datetime
from main.models import *
from utils import get_event_status_based_on_date


def get_hacks_ai_events():
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get("https://hacks-ai.ru/api/v2/hackathons/cards", headers=headers)
    data = response.json()
    events = []
    raw_events = _add_type(data["district"], "hackathons")
    raw_events.extend(_add_type(data["region"], "championships"))
    raw_events.extend(_add_type(data["federal"], "championships"))

    for raw_event in raw_events:
        event = Event()
        _fill_event(event, int(raw_event["id"]), raw_event["type"], raw_event["status"])
        events.append(event)

    return events


def _get_tasks(event_id, event_type):
    task_type = "cases" if event_type == "hackathons" else "tasks"
    response = requests.get(f"https://hacks-ai.ru/api/v2/{event_type}/{event_id}/{task_type}")
    raw_tasks = response.json()
    tasks = []

    for raw_task in raw_tasks:
        tasks.append(raw_task["name"] if event_type == "hackathons" else raw_task["title"])
    
    return tasks


def _get_event_info(event_id, event_type):
    response = requests.get(f"https://hacks-ai.ru/api/v2/{event_type}/{event_id}/info")
    return response.json()


def _fill_event(event, event_id, event_type, event_status):
    event_info = _get_event_info(event_id, event_type)
    event.address = event_info["address"]
    event.start_date = datetime.fromisoformat(event_info["startDate"]).replace(tzinfo=None)
    event.end_date = datetime.fromisoformat(event_info["endDate"]).replace(tzinfo=None)
    description = ""
    tasks = _get_tasks(event_id, event_type)

    for i in range(len(tasks)):
        description += f"{i+1}. {tasks[i]}\n"
    event.description = description

    if "img" in event_info.keys():
        event.img = event_info["img"]
    event.url = f"https://hacks-ai.ru/{event_type}/{event_id}"

    if event_type == "hackatons":
        event.title = "Хакатон"
        event.type_of_event = EventTypeClissifier.objects.get(type_code=2) # hackaton
    else:
        event.title = "Чемпионат"
        event.type_of_event = EventTypeClissifier.objects.get(type_code=6) # championship    
    
    if event_status == "registration":
        event.status_of_event = StatusOfEvent.objects.get(status_code=4) # registration
    else:
        event.status_of_event = get_event_status_based_on_date(event)


def _add_type(events, type):
    for event in events:
        event["type"] = type
    return events
