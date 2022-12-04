import html
import requests
from bs4 import BeautifulSoup
from typing import TypedDict
from dateutil.tz import tzlocal
from datetime import datetime, timezone, timedelta
from main.models import *
from .utils import get_event_types


class _EventAdditionalInfo(TypedDict):
    description: str
    is_free: bool | None
    address: str
    url: str
    start_date: datetime
    end_date: datetime


def get_ict2go_events() -> list[Event]:
    """
    Возвраащет разнообразные мероприятия с сайта:
    'https://ict2go.ru'
    """
    response = requests.get("https://ict2go.ru/events/")
    html_decoded_string = html.unescape(response.text)
    soup = BeautifulSoup(html_decoded_string, "html.parser")
    raw_events_lists = soup.find_all("div", class_="index-events")

    raw_event_list_filtered = [
        raw_events_list for raw_events_list in raw_events_lists
        if (len(raw_events_list.get("class")) == 1)
    ][0]

    raw_events = raw_event_list_filtered.find_all("div",
                                                  class_="index-events-item")

    event_types = get_event_types()
    events = []
    for raw_event in raw_events:
        event = Event()
        event.title = raw_event.find("a", class_="event-title").string

        event_url = "https://ict2go.ru" \
            f"{raw_event.find('a', class_='event-title').get('href')}"
        # event.img = "https://ict2go.ru" + raw_event.find("img").get("src")

        event_raw_type = raw_event.find("a", class_="event-type").string

        # Если данного типа мерроприятия нет в списке, то пропускаем его
        if event_raw_type not in event_types.keys():
            continue

        event.type_of_event = EventTypeClissifier \
                .objects.get(type_code=event_types[event_raw_type])

        event_additional_info = _get_event_additional_info(event_url)
        event.description = event_additional_info["description"]
        event.address = event_additional_info["address"]
        event.url = event_additional_info["url"]
        event.start_date = event_additional_info["start_date"]
        event.end_date = event_additional_info["end_date"]
        event.is_free = event_additional_info["is_free"]

        # Добавляем теги к описанию
        tags_div = raw_event.find("div", class_="event-themes")
        raw_tags = tags_div.find_all("a")
        for raw_tag in raw_tags:
            event.description += (raw_tag.string + ". ")

        # Устанавливаем московский часовой пояс
        moscow_tz = timezone(timedelta(hours=3))
        event.start_date = event.start_date.replace(tzinfo=moscow_tz)
        event.end_date = event.end_date.replace(tzinfo=moscow_tz)

        # Проверка на актуальность
        if event.start_date < datetime.now(tzlocal()).astimezone(moscow_tz):
            continue

        events.append(event)

    return events


def _get_event_additional_info(event_url: str) -> _EventAdditionalInfo:
    response = requests.get(event_url)
    html_decoded_string = html.unescape(response.text)
    soup = BeautifulSoup(html_decoded_string, "html.parser")

    raw_description = soup.find("div", class_="description-info")
    raw_description_lines = raw_description.find_all("p")
    description_lines = [raw_line.string for raw_line in raw_description_lines]
    description_lines_filtered = [
        line for line in description_lines if line is not None
    ]
    description = "\n".join(description_lines_filtered)

    url = ""
    if soup.find("a", class_="www-info") is None:
        if soup.find("a", class_="register-info") is not None:
            url = soup.find("a", class_="register-info").get("href")
        else:
            url = event_url
    else:
        url = soup.find("a", class_="www-info").get("href")

    address = soup.find("p", class_="place-info").find("a").string

    raw_date_info = soup.find("p", class_="date-info").contents[1]
    raw_date_info = raw_date_info.strip()

    raw_date_info = raw_date_info[:raw_date_info.index(". Начало")]
    raw_dates = raw_date_info.split(" - ")

    # Проверка стоимости мероприятия. Если не платное,
    # то может быть как бесплатное, так и платное
    is_free = None
    if soup.find("p", class_="price-info") is not None:
        is_free = False
    else:
        is_free = None

    start_date = datetime.now()
    end_date = datetime.now()
    if len(raw_dates) == 2:
        start_date = datetime.strptime(raw_dates[0], "%d.%m.%Y")
        end_date = datetime.strptime(raw_dates[1], "%d.%m.%Y")
    else:
        start_date = datetime.strptime(raw_dates[0], "%d.%m.%Y")
        end_date = datetime.strptime(raw_dates[0], "%d.%m.%Y")

    return _EventAdditionalInfo(description=description,
                                is_free=is_free,
                                address=address,
                                url=url,
                                start_date=start_date,
                                end_date=end_date)
