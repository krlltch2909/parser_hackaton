import requests
from dateutil.tz import tzlocal
from datetime import datetime, timedelta, timezone, timedelta
from main.models import *
from .utils import get_event_types


HACKATHONS = "hackathons"
CHAMPIOMSHIPS = "championships"


def get_hacks_ai_events() -> list[Event]:
    """
    Возвращает хакатоны и чемпионаты с сайта:
    'https://hacks-ai.ru'
    """
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


def _get_tasks(event_id: int, event_type: str) -> list[str]:
    task_type = "cases" if event_type == HACKATHONS else "tasks"
    response = requests.get(f"https://hacks-ai.ru/api/v2/{event_type}/{event_id}/{task_type}")
    raw_tasks = response.json()
    tasks = []

    for raw_task in raw_tasks:
        tasks.append(raw_task["name"] if event_type == HACKATHONS else raw_task["title"])
    
    return tasks


def _get_event_info(event_id: int, event_type) -> dict:
    response = requests.get(f"https://hacks-ai.ru/api/v2/{event_type}/{event_id}/info")
    return response.json()


def _fill_event(event: Event, event_id: int, event_type: str) -> bool:
    event_types = get_event_types()
    event_info = _get_event_info(event_id, event_type)

    if "registrationDeadline" not in event_info.keys():
        return False

    event.address = event_info["address"]

    event.registration_deadline = datetime.fromisoformat(event_info["registrationDeadline"])

    # Переводим в московское время    
    moscow_tz = timezone(timedelta(hours=3))
    event.registration_deadline = event.registration_deadline.astimezone(moscow_tz)

    # Проверка на актуальность
    if event.registration_deadline < datetime.now(tzlocal()).astimezone(moscow_tz):
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
        event.title = f"'Цифровой прорыв'. Хакатон ({event.address})"
        
        if "Хакатон" not in event_types.keys():
            return False

        event.type_of_event = EventTypeClissifier.objects.get(description="Хакатон")
    else:
        event.title = f"'Цифровой прорыв'. Чемпионат ({event.address})"
        
        if "Соревнование" not in event_types.keys():
            return False

        event.type_of_event = EventTypeClissifier.objects.get(description="Соревнование")

    event.is_free = True
    return True


def _add_type(raw_events: list[dict], type: str) -> list[dict]:
    for event in raw_events:
        event["type"] = type
    return raw_events


def _check_availability(event_url: str) -> bool:
    response = requests.get(event_url)
    return response.status_code != 404
