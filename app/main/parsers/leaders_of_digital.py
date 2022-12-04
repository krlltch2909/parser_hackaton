import requests
from dateutil.tz import tzlocal
from datetime import datetime, timezone, timedelta
from main.models import *
from .utils import get_event_types


def get_leaders_of_digital_events() -> list[Event]:
    """
    Возвращает список событий с сайта:
    https://leadersofdigital.ru
    """
    response = requests.get(
        "https://leadersofdigital.ru/api/v1/site_get_all/0")
    data = response.json()
    raw_events = data["event"]
    event_types = get_event_types()
    events = []

    for raw_event in raw_events:
        event = Event()

        if "registration_deadline_date" not in raw_event.keys():
            continue

        event.title = raw_event["name"]
        event.description = raw_event["description"]
        event.registration_deadline = datetime.fromisoformat(
            raw_event["registration_deadline_date"])

        # Переводим в московское время
        moscow_tz = timezone(timedelta(hours=3))
        event.registration_deadline = event.registration_deadline.astimezone(
            moscow_tz)

        # Проверка на актуальность
        if event.registration_deadline < datetime.now(
                tzlocal()).astimezone(moscow_tz):
            continue

        event.url = f'https://leadersofdigital.ru/event/{raw_event["event_id"]}'
        # event.img = raw_event["avatar_big_url"]

        if "Соревнование" not in event_types.keys():
            continue

        event.type_of_event = EventTypeClissifier.objects.get(
            description="Соревнование")
        event.is_free = True
        events.append(event)

    return events
