import json
import re
import requests
from datetime import datetime, timezone, timedelta
from main.models import *
from .utils import event_types, CLEANER


_themeIds = [
    603, 599, 608, 610, 602, 606, 609, 605, 612,
    600, 604, 1227, 601, 613, 607, 611, 749,
    742, 36, 745, 37, 698, 753, 751
]

def get_leader_id_events() -> list:
    """
    Возвращает список событий с сайта:
    'https://leader-id.ru'
    """
    base_url = "https://leader-id.ru/api/v4/events/search?expand=photo, themes, type, place&sort=date&actual=1&registrationActual=1&paginationSize=10"

    additional_url = ""
    for themeId in _themeIds:
        additional_url += f"&themeIds[]={themeId}"

    url = base_url + additional_url
    response = requests.get(url + "&paginationPage=1")
    data = response.json()

    raw_events = []
    while response.status_code != 422:
        raw_events.extend(data["data"]["_items"])
        current_page = data["data"]["_meta"]["currentPage"]

        response = requests.get(url + f"&paginationPage={current_page+1}")
        data = response.json()

    events = []
    for raw_event in raw_events:
        event = Event()

        if raw_event["timezone"] is None:
            continue

        event_raw_type = raw_event["type"]["name"]
        
        # Если данного типа мерроприятия нет в списке, то пропускаем его
        if event_raw_type not in event_types.keys():
            continue

        event.title = raw_event["full_name"]
        event_description_info = json.loads(raw_event["full_info"])
        description = ""
        for description_block in event_description_info["blocks"]:
            description_block_data = description_block["data"]
            if "text" in description_block_data.keys():
                description += re.sub(CLEANER, "", description_block["data"]["text"])
        
        event.description = description

        local_tz = timezone(timedelta(minutes=raw_event["timezone"]["minutes"]))
            
        event.start_date = datetime.strptime(
            raw_event["date_start"], 
            "%Y-%m-%d %H:%M:%S"
        )
        event.start_date = event.start_date.replace(tzinfo=local_tz)
        event.end_date = datetime.strptime(
            raw_event["date_end"], 
            "%Y-%m-%d %H:%M:%S"
        )
        event.end_date = event.end_date.replace(tzinfo=local_tz)

        # Переводим в московское время
        moscow_tz = timezone(timedelta(hours=3))
        event.start_date = event.start_date.astimezone(moscow_tz)
        event.end_date = event.end_date.astimezone(moscow_tz)

        event.url = f"https://leader-id.ru/events/{raw_event['id']}"
        event.img = raw_event["photo"]

        if raw_event["format"] != "online":
            if raw_event["space"] is not None:
                event.address = raw_event["space"]["address"]["title"]

        event.type_of_event = EventTypeClissifier \
                .objects.get(type_code=event_types[event_raw_type])

        events.append(event)

    return events
