import requests
from datetime import datetime
from main.models import *


HACKATHONS = "hackathons"
CHAMPIOMSHIPS = "championships"


def get_hacks_ai_events():
    response = requests.get("https://hacks-ai.ru/api/v2/hackathons/cards")
    data = response.json()
    raw_events = _add_type(data["district"], HACKATHONS)
    raw_events.extend(_add_type(data["region"], CHAMPIOMSHIPS))
    raw_events.extend(_add_type(data["federal"], CHAMPIOMSHIPS))
    events = []

    for raw_event in raw_events:
        event = Event()
        fill_status = _fill_event(event, int(raw_event["id"]), raw_event["type"])
        if fill_status:
            events.append(event)

    return events


def _get_tasks(event_id, event_type):
    task_type = "cases" if event_type == HACKATHONS else "tasks"
    response = requests.get(f"https://hacks-ai.ru/api/v2/{event_type}/{event_id}/{task_type}")
    raw_tasks = response.json()
    tasks = []

    for raw_task in raw_tasks:
        tasks.append(raw_task["name"] if event_type == HACKATHONS else raw_task["title"])
    
    return tasks


def _get_event_info(event_id, event_type):
    response = requests.get(f"https://hacks-ai.ru/api/v2/{event_type}/{event_id}/info")
    return response.json()


def _fill_event(event, event_id, event_type):
    event_info = _get_event_info(event_id, event_type)

    if "registrationDeadline" not in event_info.keys():
        return False

    event.address = event_info["address"]
    event.registration_deadline = datetime.fromisoformat(event_info["registrationDeadline"]) \
        .replace(tzinfo=None)

    if event.registration_deadline < datetime.now():
        return False

    description = ""
    tasks = _get_tasks(event_id, event_type)

    for i in range(len(tasks)):
        description += f"{i+1}. {tasks[i]}\n"
    event.description = description

    if "img" in event_info.keys():
        event.img = event_info["img"]
    event.url = f"https://hacks-ai.ru/{event_type}/{event_id}"

    if not _check_availability(event.url):
        return False

    if event_type == HACKATHONS:
        event.title = "Хакатон"
        event.type_of_event = EventTypeClissifier.objects.get(type_code=2) # hackathon
    else:
        event.title = "Чемпионат"
        event.type_of_event = EventTypeClissifier.objects.get(type_code=6) # championship    

    event.status_of_event = StatusOfEvent.objects.get(status_code=4) # registration
    return True


def _add_type(events, type):
    for event in events:
        event["type"] = type
    return events


def _check_availability(event_url):
    response = requests.get(event_url)
    return response.status_code != 404
