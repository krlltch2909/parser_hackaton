import os
import re
import requests
from dateutil.tz import tzlocal
from datetime import datetime, timedelta, timezone, timedelta
from main.models import *
from utils import CLEANER


def get_hackathon_com_events() -> list:
    """
    Возвращает список хакатонов с сайта:
    'https://xn--80aa3anexr.com/?ysclid=l8dfsnhzg4886000894'
    """
    feeduid = os.environ.get("FEEDUID")
    response = requests.get(f"https://feeds.tildacdn.com/api/getfeed/?feeduid={feeduid}&feedtz=Europe/Moscow")
    data = response.json()

    events = []
    for raw_event in data["posts"]:
        event = Event()
        event.title = raw_event["title"]

        # Очистка текста от html-тегов и других символов
        event.description = re.sub(CLEANER, "", raw_event["descr"])
        event.registration_deadline = datetime.strptime(raw_event["date"], "%Y-%m-%d %H:%M")

        # Установка московского часового пояса
        moscow_tz = timezone(timedelta(hours=3))
        event.registration_deadline = event.registration_deadline.astimezone(moscow_tz)

        # Проверка на актуальность
        if event.registration_deadline < datetime.now(tzlocal()).astimezone(moscow_tz):
            continue

        event.url = raw_event["url"]
        event.img = raw_event["image"]

        event.type_of_event = EventTypeClissifier.objects.get(type_code=2)  # Хакатон
        events.append(event)
    
    return events
