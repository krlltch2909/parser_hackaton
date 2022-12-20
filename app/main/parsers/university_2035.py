import html
import re
import requests
from enum import Enum
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from typing import TypedDict
from main.models import *
from .utils import HTML_TAG_CLEANER, get_event_types


class _AcceleratorStatus(Enum):
    IN_PROCESS = "Идет акселерация"
    REGISTRATION = "Готовится к открытию"
    CLOSED = "Закрыт"


class _EventAdditionalInfo(TypedDict):
    description: str
    start_date: datetime
    end_date: datetime


direction_tags = [
    "5886f7db-e0c8-47db-8d3b-fe830ec788dd"  # IT
]


def get_2035_university_events() -> list[Event]:
    """
    Возвращает акселераторы с сайта:
    https://pt.2035.university/accelerator
    """

    base_url = "https://pt.2035.university"

    additional_url = ""
    for direction_tag in direction_tags:
        additional_url += f"&directionTags[]={direction_tag}"

    url = base_url + "/accelerator/index?" + additional_url
    response = requests.get(url)
    html_decoded_string = html.unescape(response.text)
    soup = BeautifulSoup(html_decoded_string, "html.parser")
    raw_pages_links = soup.find_all("a", class_="page-link")

    # Получение номеров всех страниц
    pages_additional_urls = set([
        raw_page_link.get("href") for raw_page_link in raw_pages_links
        if raw_page_link
    ])
    pages_urls = list(map(lambda x: base_url + x, pages_additional_urls))

    event_types = get_event_types()
    events = []

    if "Акселератор" not in event_types.keys():
        return events

    for page_url in pages_urls:
        response = requests.get(page_url)
        html_decoded_string = html.unescape(response.text)
        page = BeautifulSoup(html_decoded_string, "html.parser")
        page_raw_events = page.find_all("a", class_="accelerator-item")

        for page_raw_event in page_raw_events:
            event = Event()
            
            event_status_div = page_raw_event.find("div", class_="accelerator__tag")
            event_status =  _get_event_status(event_status_div.string)            
            if event_status == _AcceleratorStatus.CLOSED:
                continue
            
            event.title = page_raw_event.find("h4").string
            event.url = base_url + page_raw_event.get("href")
            event_additional_info = _get_event_additional_info(event.url, event_status)
            
            if event_additional_info is None:
                continue

            event.description = event_additional_info["description"]
            event.start_date = event_additional_info["start_date"]
            event.end_date = event_additional_info["end_date"]
            
            # Устанавливаем московский часововой пояс
            moscow_tz = timezone(timedelta(hours=3))
            event.start_date = event.start_date.replace(tzinfo=moscow_tz)
            event.end_date = event.end_date.replace(tzinfo=moscow_tz)
            
            # Проверка на актуальность
            if event.end_date < datetime.now(tzlocal()).astimezone(moscow_tz):
                continue
             
            event.type_of_event = EventTypeClissifier \
                .objects.get(type_code=event_types["Акселератор"])

            event.is_free = True

            events.append(event)

    return events


def _get_event_status(raw_event_status: str) -> _AcceleratorStatus:
    if raw_event_status == _AcceleratorStatus.IN_PROCESS.value:
        return _AcceleratorStatus.IN_PROCESS
    elif raw_event_status == _AcceleratorStatus.REGISTRATION.value:
        return _AcceleratorStatus.REGISTRATION
    else:
        return _AcceleratorStatus.CLOSED


def _get_event_additional_info(event_url: str, 
                               event_status: _AcceleratorStatus) -> _EventAdditionalInfo | None:
    """
    Возвращает None, если нет информации о датах проведения (мероприятие стоит пропустить)
    """
    response = requests.get(event_url)
    html_decoded_string = html.unescape(response.text)
    event_page = BeautifulSoup(html_decoded_string, "html.parser")

    description = ""

    h3_tags = event_page.find_all("h3")
    description_headers_list = [
        h for h in h3_tags
        if h.string is not None and "Об акселераторе:" in h.string
    ]
    if len(description_headers_list) != 0:
        description_header_parent = description_headers_list[0].parent
        description_paragraphs = []
        for child_tag in description_header_parent.find_all(recursive=False):
            if child_tag.name == "p":
                description_paragraphs.append(str(child_tag))
            elif len(description_paragraphs) > 0:
                break

        description = ""
        for description_paragraph in description_paragraphs:
            description += f"\n{re.sub(HTML_TAG_CLEANER, '', description_paragraph)}"

    all_bold_tags = event_page.find_all("b")
    # Добавляем теги
    tags_divs = event_page.find_all(class_="accelerator__tag")
    for tag_div in tags_divs:
        description += tag_div.string
    
    if event_status == _AcceleratorStatus.IN_PROCESS or \
        event_status == _AcceleratorStatus.REGISTRATION:  
        date_paragraph_list = [
            b.parent for b in all_bold_tags if "Даты проведения" in b.string
        ]
        if len(date_paragraph_list) != 0:
            date_paragraph = date_paragraph_list[0]
            date_string = date_paragraph.contents[2] \
                                        .strip(" \n") \
                                        .replace(" ", "") \
                                        .replace("\n", "")

            date_strings = date_string.split("-")
            start_date = datetime.strptime(date_strings[0], "%d.%m.%Y")
            end_date = datetime.strptime(date_strings[1], "%d.%m.%Y")
            
            # Устанавливаем московский часововой пояс
            moscow_tz = timezone(timedelta(hours=3))
            start_date = start_date.replace(tzinfo=moscow_tz)
            end_date = end_date.replace(tzinfo=moscow_tz)

            return _EventAdditionalInfo(description=description,
                                        start_date=start_date,
                                        end_date=end_date)
    return None
