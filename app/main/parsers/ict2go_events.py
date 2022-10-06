import requests
import html
from dateutil.tz import tzlocal
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from main.models import *
from utils import event_types


def get_ict2go_events() -> list:
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

    raw_events = raw_event_list_filtered.find_all("div", class_="index-events-item")

    events = []
    for raw_event in raw_events:
        event = Event()
        event.title = raw_event.find("a", class_="event-title").string

        event_url = "https://ict2go.ru" \
            f"{raw_event.find('a', class_='event-title').get('href')}"
        event.img = "https://ict2go.ru" + raw_event.find("img").get("src")

        event_raw_type = raw_event.find("a", class_="event-type").string

        # Если данного типа мерроприятия нет в списке, то пропускаем его
        if event_raw_type not in event_types.keys:
            continue

        event.type_of_event = EventTypeClissifier \
                .objects.get(type_code=event_types[event_raw_type])

        event_additional_info = _get_event_additional_info(event_url)
        event.description = event_additional_info["description"]
        event.address = event_additional_info["address"]
        event.url = event_additional_info["url"]
        event.start_date = event_additional_info["start_date"]
        event.end_date = event_additional_info["end_date"]

        # Устанавливаем московский часовой пояс
        moscow_tz = timezone(timedelta(hours=3))
        event.start_date = event.start_date.replace(tzinfo=moscow_tz)
        event.end_date = event.end_date.replace(tzinfo=moscow_tz)

        # Проверка на актуальность
        if event.start_date < datetime.now(tzlocal()).astimezone(moscow_tz):
            continue
        
        events.append(event)

    return events


def _get_event_additional_info(event_url: str) -> dict:
    result = {}

    response = requests.get(event_url)
    html_decoded_string = html.unescape(response.text)
    soup = BeautifulSoup(html_decoded_string, "html.parser")

    raw_description = soup.find("div", class_="description-info")
    raw_description_lines = raw_description.find_all("p")
    description_lines = [raw_line.string for raw_line in raw_description_lines]
    description_lines_filtered = [line for line in description_lines if line is not None]
    description = "\n".join(description_lines_filtered)
    result["description"] = description

    if soup.find("a", class_="www-info") is None:
        if soup.find("a", class_="register-info") is not None:
            result["url"] = soup.find("a", class_="register-info").get("href")
        else:
            result["url"] = event_url
    else:
        result["url"] = soup.find("a", class_="www-info").get("href")

    address = soup.find("p", class_="place-info").find("a").string
    result["address"] = address

    raw_date_info = soup.find("p", class_="date-info").contents[1]
    raw_date_info = raw_date_info.strip()

    raw_date_info = raw_date_info[:raw_date_info.index(". Начало")]
    raw_dates = raw_date_info.split(" - ")

    if len(raw_dates) == 2:
        result["start_date"] = datetime.strptime(raw_dates[0], "%d.%m.%Y")
        result["end_date"] = datetime.strptime(raw_dates[1], "%d.%m.%Y")
    else:
        result["start_date"] = datetime.strptime(raw_dates[0], "%d.%m.%Y")
        result["end_date"] = datetime.strptime(raw_dates[0], "%d.%m.%Y")

    return result
