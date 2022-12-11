import html
import re
import requests
from bs4 import BeautifulSoup
from dateutil.tz import tzlocal
from datetime import datetime, timezone, timedelta
from main.models import *
from .utils import get_event_types, HTML_TAG_CLEANER


def get_all_events() -> list[Event]:
    """
    Возвращает список различных событий с сайта:
    'https://all-events.ru/events/'
    """
    event_types = get_event_types()
    events = []

    url = "https://all-events.ru/events/calendar/theme-is-upravlenie_personalom_hr-or-informatsionnye_tekhnologii-or-automotive_industry-or-bezopasnost-or-blokcheyn_kriptovalyuty-or-innovatsii-or-it_telecommunications-or-elektronnaya_kommertsiya/type-is-conferencia-or-hackathon-or-contest/"
    response = requests.get(url)
    html_decoded_string = html.unescape(response.text)
    first_page = BeautifulSoup(html_decoded_string, "html.parser")
    navigation_pages = first_page.find(name="div", attrs={"class": "navigation-pages"})\
        .find_all(name="a")
    raw_pages = [first_page]
    for navigation_page in navigation_pages:
        page_address = f"{url}?PAGEN_1={navigation_page.string}"
        response = requests.get(page_address)
        raw_page = BeautifulSoup(response.text, "html.parser")
        raw_pages.append(raw_page)

    # Для каждой html страницы получаем свои события
    for raw_page in raw_pages:
        raw_events_list_element = raw_page \
            .find(name="div", class_="events-list")

        raw_events_list = raw_events_list_element\
            .find_all("div", class_="event-wrapper")
        raw_events_additional_info_list = raw_events_list_element\
            .find_all("div", class_="event")

        raw_events = [(raw_events_list[i], raw_events_additional_info_list[i]) \
                       for i in range(len(raw_events_list))]

        for raw_event, event_additional_data in raw_events:
            event = Event()
            event.title = raw_event \
                .find(name="div", class_="event-title") \
                .string
            description_items = raw_event \
                .find(name="span", attrs={"itemprop": "description"}).contents

            description = ""
            for description_item in description_items:
                description += re.sub(HTML_TAG_CLEANER, "", str(description_item)\
                    .strip(" \n\t\r")) + "\n"

            description = description.replace("\t", "")
            description = description.replace("\r", "")
            description = description.replace("\n\n\n", "\n")
            description = description.replace("\n\n", "\n")
            event.description = description

            # Добавляем теги к описанию
            tags_div = event_additional_data.find("div", class_="news-topics")
            if tags_div is not None:
                raw_tags = tags_div.find_all("a")
                for raw_tag in raw_tags:
                    event.description += (". " + raw_tag.string)

            raw_start_date = raw_event.find(name="div",
                                            attrs={"itemprop": "startDate"}) \
                                      .get("content")
            event.start_date = datetime.fromisoformat(raw_start_date)
            raw_end_date = raw_event.find(name="div",
                                          attrs={"itemprop": "endDate"}) \
                                    .get("content")
            event.end_date = datetime.fromisoformat(raw_end_date)

            # Переводим в московское время
            moscow_tz = timezone(timedelta(hours=3))
            event.start_date = event.start_date.astimezone(moscow_tz)
            event.end_date = event.end_date.astimezone(moscow_tz)

            #  Проверка на актуальность
            if event.start_date < datetime.now(
                    tzlocal()).astimezone(moscow_tz):
                continue

            event.url = "https://all-events.ru" \
                + raw_event.find(name="a", attrs={"itemprop": "url"}) \
                           .get("href")
            # event.img = "https://all-events.ru"  \
            # + raw_event.find(name="img").get("src")
            event.address = raw_event.find(name="div", class_="event-venue") \
                                     .find(name="div", class_="address") \
                                     .find(name="span", attrs={"itemprop": "addressLocality"}) \
                                     .string

            raw_event_type = event_additional_data.find(
                "div", class_="event-type").string

            # Если данного типа мерроприятия нет в списке, то пропускаем его
            if raw_event_type not in event_types.keys():
                continue

            event.type_of_event = EventTypeClissifier \
                .objects.get(type_code=event_types[raw_event_type])

            # Вычисление стоимости мероприятия
            raw_event_cost_type = raw_event.find("div", class_="event-price") \
                                           .get("content") \
                                           .strip(" ")

            if raw_event_cost_type == "Бесплатно":
                event.is_free = True
            elif raw_event_cost_type != "" \
                and raw_event_cost_type[len(raw_event_cost_type)-1].isdigit():
                event.is_free = False

            events.append(event)

    return events
