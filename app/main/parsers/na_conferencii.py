import html
import locale
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag as BS4Tag
from dateutil.tz import tzlocal
from datetime import datetime, timezone, timedelta
from typing import TypedDict
from main.models import *
from .utils import get_event_types, get_tag_types


class _EventAdditionalInfo(TypedDict):
    description: str
    is_free: bool | None
    event_tags: list[str]


# Категории мероприятий
categories = [
    "Информационные технологии", "Биотехнологии", "Технологии",
    "Технические науки (Разное)"
]

# Категории вхождения в наукометрические базы
ref_categories = {
    "РИНЦ": 4,
    "Перечень ВАК": 5,
    "Scopus": 6,
    "Web of Science": 7,
}

# Ключевые слова для выявления стоимости мероприятия
keywords = {
    "paid": {
        "words": [
            "руб.",
            "рублей",
        ],
        "regex": [
            "\d р.",
        ]
    },
    "free": {
        "words": [
            "бесплатн",
        ],
        "regex": [".*взнос.*не предусм.*"]
    }
}


def get_na_conferencii_events() -> list[Event]:
    """
    Возвращает конференции с сайта: 
    https://na-konferencii.ru/
    """
    url = "https://na-konferencii.ru/conference-type/konferencii"

    response = requests.post(url)
    html_decoded_string = html.unescape(response.text)
    page = BeautifulSoup(html_decoded_string, "html.parser")
    pages = [page]

    page_paragraphs = page.find_all("a", class_="page-numbers")
    if len(page_paragraphs) > 1:
        end_page_number = int(page_paragraphs[-2].string)
        for i in range(2, end_page_number + 1):
            response = requests.post(url + f"/page/{i}")
            html_decoded_string = html.unescape(response.text)
            page = BeautifulSoup(html_decoded_string, "html.parser")
            pages.append(page)
    events = []
    for page in pages:
        page_raw_events = page.find_all("div", class_="notice-item")

        for page_raw_event in page_raw_events:

            event = _get_event(page_raw_event)

            if event is not None:
                events.append(event)

    return events


def _get_event(raw_event: BS4Tag) -> Event | None:
    event_types = get_event_types()
    event = Event()

    event_date_block = raw_event \
        .find("div", class_="notice-item-top-date") \
        .find("p")

    event_raw_date = event_date_block.contents[0].strip(" \n")
    event_raw_date_splitted = event_raw_date.split(" - ")
    start_date_day = event_raw_date_splitted[0].split(" ")[0]
    start_date_month = event_raw_date_splitted[0].split(" ")[1]
    end_date_day = event_raw_date_splitted[1].split(" ")[0]
    end_date_month = event_raw_date_splitted[1].split(" ")[1]
    date_year = event_raw_date_splitted[1].split(" ")[2]

    # Получаем данные для даты окончания регистрации
    event_raw_registration_deadline = event_date_block \
        .contents[len(event_date_block.contents)-1].strip(" \n")
    raw_registration_shortened = \
        event_raw_registration_deadline[
            event_raw_registration_deadline.index("по"):
        ]
    raw_registration_splitted = raw_registration_shortened.split(" ")
    registration_day = raw_registration_splitted[1]
    registration_month = raw_registration_splitted[2]
    registration_year = raw_registration_splitted[3]

    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
    event.start_date = datetime\
        .strptime(f"{start_date_day} {start_date_month} {date_year}", "%d %B %Y")
    event.end_date = datetime\
        .strptime(f"{end_date_day} {end_date_month} {date_year}", "%d %B %Y")
    event.registration_deadline = datetime\
        .strptime(f"{registration_day} {registration_month} {registration_year}", "%d %B %Y")

    # Устанавливаем московский часововой пояс
    moscow_tz = timezone(timedelta(hours=3))
    event.start_date = event.start_date.replace(tzinfo=moscow_tz)
    event.end_date = event.end_date.replace(tzinfo=moscow_tz)
    event.registration_deadline = event.registration_deadline.replace(
        tzinfo=moscow_tz)

    # Проверка на актуальность
    if event.registration_deadline < datetime.now(
            tzlocal()).astimezone(moscow_tz):
        return None

    event.title = raw_event \
        .find("div", class_="notice-item-title").find("a").string
    event.url =  raw_event \
        .find("div", class_="notice-item-title").find("a").get("href")
    event.address = raw_event \
        .find("div", class_="notice-item-top-location") \
        .find("p").string

    is_valid_event, event_additional_info = _get_event_additional_info(
        event.url)
    if not is_valid_event:
        return None

    event.description = event_additional_info["description"]

    # Добавляем теги к описанию
    tags_div = raw_event.find("div", class_="notice-item-body-inner")
    raw_tags = tags_div.find_all("a")
    for raw_tag in raw_tags:
        event.description += (". " + raw_tag.string)

    if "Конференция" not in event_types.keys():
        return None

    event.type_of_event = EventTypeClissifier \
        .objects.get(type_code=event_types["Конференция"])

    event.is_free = event_additional_info["is_free"]

    return event


def _get_event_additional_info(
        event_url: str) -> tuple[bool, _EventAdditionalInfo]:
    tag_types = get_tag_types()

    response = requests.get(event_url)
    html_decoded_string = html.unescape(response.text)
    page = BeautifulSoup(html_decoded_string, "html.parser")

    description_paragraphs = page \
        .find("div", class_="content-page-body") \
        .find_all("p", recursive=False)
    description = ""
    alternative_description = page.find("meta", attrs={
        "name": "description"
    }).get("content")

    for paragraph in description_paragraphs:
        if paragraph.string is not None:
            description += f"\n{paragraph.string}"

    header = page.find("div", class_="content-page-header-inner")
    raw_tags = header.find_all("a")
    tags = [raw_tag.string for raw_tag in raw_tags]

    is_valid_event = False
    for category_name in categories:
        if category_name in tags:
            is_valid_event = True

    event_tags = []

    for tag_type_name in tag_types.keys():
        if tag_type_name in tags:
            event_tags.append(tag_type_name)

    description = description \
        if len(description) > len(alternative_description) \
        else alternative_description

    # Вычисление стоимости конференции
    is_free = None
    for word in keywords["paid"]["words"]:
        if word in description.lower():
            is_free = False

    for regex in keywords["paid"]["regex"]:
        if re.search(regex, description.lower()):
            is_free = False

    for word in keywords["free"]["words"]:
        if word in description.lower():
            is_free = True

    for regex in keywords["free"]["regex"]:
        if re.search(regex, description.lower()):
            is_free = True

    return (is_valid_event,
            _EventAdditionalInfo(description=description,
                                 is_free=is_free,
                                 event_tags=event_tags))
