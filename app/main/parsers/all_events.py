import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from main.models import *


def get_all_events():
    headers = {
        "User-Agent": os.environ.get("USER_AGENT")
    }
    response = requests.get("https://all-events.ru/events/calendar/theme-is-informatsionnye_tekhnologii/type-is-conferencia/", headers=headers)
    first_page = BeautifulSoup(response.text, "html.parser")
    navigation_pages = first_page.find(name="div", attrs={"class": "navigation-pages"}) \
        .find_all(name="a")
    raw_pages = [first_page]
    for navigation_page in navigation_pages:
        page_address = f"https://all-events.ru/events/calendar/" \
            "theme-is-informatsionnye_tekhnologii/type-is-conferencia/" \
            f"?PAGEN_1={navigation_page.string}"
        response = requests.get(page_address, headers=headers)
        raw_page = BeautifulSoup(response.text, "html.parser")
        raw_pages.append(raw_page)

    events = []
    for raw_page in raw_pages:
        page_raw_events = raw_page.find_all(name="div", 
                                            attrs={"class": "event-wrapper"})
        for raw_event in page_raw_events:
            event = Event()
            event.title = raw_event \
                .find(name="div", class_="event-title") \
                .string
            event.description = raw_event \
                .find(name="span", attrs={"itemprop": "description"}) \
                .string
            event.description = event.description.strip()
            raw_start_date = raw_event.find(name="div", 
                                            attrs={"itemprop": "startDate"}) \
                                      .get("content")
            event.start_date = datetime.fromisoformat(raw_start_date) \
                .replace(tzinfo=None)
            raw_end_date = raw_event.find(name="div", 
                                          attrs={"itemprop": "endDate"}) \
                                    .get("content")
            event.end_date = datetime.fromisoformat(raw_end_date) \
                .replace(tzinfo=None)
            event.url = "https://all-events.ru" \
                + raw_event.find(name="a", attrs={"itemprop": "url"}) \
                           .get("href")
            event.img = "https://all-events.ru"  \
                + raw_event.find(name="img").get("src")
            event.address = raw_event.find(name="div", class_="event-venue") \
                                     .find(name="div", class_="address") \
                                     .string
            event.type_of_event = EventTypeClissifier.objects.get(type_code=1)  # conference 
            event.status_of_event = StatusOfEvent.objects.get(status_code=3)  # unavailable
            events.append(event)
    
    return events
