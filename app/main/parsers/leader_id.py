import json
import re
import requests
from datetime import datetime, timezone, timedelta
from main.models import *
from .utils import get_event_types, CLEANER

_themeIds = [1227, 749, 742, 36, 745, 37, 753, 751, 50]


def get_leader_id_events() -> list[Event]:
    """
    Возвращает список событий с сайта:
    'https://leader-id.ru'
    """
    page_size = 10
    base_url = "https://leader-id.ru/api/v4/events/search?expand=photo, themes, type, place&sort=date&actual=1&registrationActual=1"
    base_url += f"&paginationSize={page_size}"

    additional_url = ""
    for themeId in _themeIds:
        additional_url += f"&themeIds[]={themeId}"

    url = base_url + additional_url
    response = requests.get(url + "&paginationPage=1")
    data = response.json()
    pages_count = data["data"]["_meta"]["pageCount"]
    raw_events = []

    for i in range(2, pages_count + 1):
        try:
            raw_events.extend(data["data"]["_items"])
        except KeyError:
            break
        response = requests.get(url + f"&paginationPage={i}")
        data = response.json()

    events = []
    for raw_event in raw_events:
        event = _get_event(raw_event)

        if event is not None and event not in events:
            events.append(event)

    return events


def _get_event(raw_event: dict) -> Event | None:
    """
    Создает объект Event на основании переданного словаря с данными.
    Если данные не удовлетворяют требованиям, то возвращается None
    """
    event_types = get_event_types()
    event = Event()

    if raw_event["timezone"] is None:
        return None

    if raw_event["type"] is None:
        return None

    # Если данного типа мерроприятия нет в списке, то пропускаем его
    event_raw_type = raw_event["type"]["name"]
    if event_raw_type not in event_types.keys():
        return None

    event.title = raw_event["full_name"]

    event_description_info = json.loads(raw_event["full_info"])
    description = ""
    for description_block in event_description_info["blocks"]:
        description_block_data = description_block["data"]
        if "text" in description_block_data.keys():
            description += re.sub(CLEANER, "",
                                  description_block["data"]["text"] + "\n")

    event.description = description

    # Добавляем темы к описанию. Для более точной работы теггера
    raw_themes = raw_event["themes"]
    for raw_theme in raw_themes:
        event.description += f"{raw_theme['name']}. "

    local_tz = timezone(timedelta(minutes=raw_event["timezone"]["minutes"]))

    event.start_date = datetime.strptime(raw_event["date_start"],
                                         "%Y-%m-%d %H:%M:%S")
    event.start_date = event.start_date.replace(tzinfo=local_tz)
    event.end_date = datetime.strptime(raw_event["date_end"],
                                       "%Y-%m-%d %H:%M:%S")
    event.end_date = event.end_date.replace(tzinfo=local_tz)

    # Переводим в московское время
    moscow_tz = timezone(timedelta(hours=3))
    event.start_date = event.start_date.astimezone(moscow_tz)
    event.end_date = event.end_date.astimezone(moscow_tz)

    event.url = f"https://leader-id.ru/events/{raw_event['id']}"
    # event.img = raw_event["photo"]

    # Если указан адрес, то добавляем его
    if raw_event["format"] != "online":
        if raw_event["space"] is not None:
            event.address = raw_event["space"]["address"]["title"]

    event.type_of_event = EventTypeClissifier \
            .objects.get(type_code=event_types[event_raw_type])

    return event
