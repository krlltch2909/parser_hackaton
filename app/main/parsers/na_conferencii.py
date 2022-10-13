import html
import locale
import requests
from bs4 import BeautifulSoup
from dateutil.tz import tzlocal
from datetime import datetime, timezone, timedelta
from main.models import *
from .utils import event_types, tag_types

# Категории мероприятий
categories = {
    "Информационные технологии": 106,
    "Биотехнологии": 107,
}

# Категории вхождения в наукометрические базы
ref_categories = {
    "РИНЦ": 4,
    "Перечень ВАК": 5,
    "Scopus": 6,
    "Web of Science": 7,
}


def get_na_conferencii_events() -> list:
    """
    Возвращает конференции с сайта: 
    https://na-konferencii.ru/
    """
    url = "https://na-konferencii.ru/wp-admin/admin-ajax.php"

    # Строка для более конкретного поиска по сайту
    base_data_string= f"action=filterhome&nonce={_get_nonce_key()}"
    for category in categories.values():
        base_data_string += f"&category%5B%5D={category}"
    
    now = datetime.now()
    # Необходимо искать концеренции, начало которых не позже текущей даты
    base_data_string += f"&period_start={now.day}%2F{now.month}%2F{now.year}"

    for ref_category in ref_categories.values():
        base_data_string += f"&ref_category%5B%5D={ref_category}"

    # Ведем поиск только конференций
    base_data_string += "&search_type=konferencii"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=base_data_string + "&page=1", headers=headers)
    html_decoded_string = html.unescape(response.text)
    page = BeautifulSoup(html_decoded_string, "html.parser")
    pages = [page]

    page_paragraphs = page.find_all("a", class_="page-numbers")
    if len(page_paragraphs) > 1:
        end_page_number = int(page_paragraphs[-2].string)
        for i in range(2, end_page_number+1):
            response = requests.post(url, data=base_data_string + f"&page={i}", headers=headers)
            html_decoded_string = html.unescape(response.text)
            page = BeautifulSoup(html_decoded_string, "html.parser")
            pages.append(page)
    events = []
    for page in pages:
        page_raw_events = page.find_all("div", class_="notice-item")

        for page_raw_event in page_raw_events:
            event = Event()
            
            event_date_block = page_raw_event \
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

            locale.setlocale(locale.LC_TIME, "ru_RU")
            event.start_date = datetime.strptime(f"{start_date_day} {start_date_month} {date_year}", "%d %B %Y")
            event.end_date = datetime.strptime(f"{end_date_day} {end_date_month} {date_year}", "%d %B %Y")
            event.registration_deadline = datetime.strptime(f"{registration_day} {registration_month} {registration_year}", "%d %B %Y")

            # Устанавливаем московский часововой пояс
            moscow_tz = timezone(timedelta(hours=3))
            event.start_date = event.start_date.replace(tzinfo=moscow_tz)
            event.end_date = event.end_date.replace(tzinfo=moscow_tz)      
            event.registration_deadline = event.registration_deadline.replace(tzinfo=moscow_tz)      

            event.title = page_raw_event \
                .find("div", class_="notice-item-title").find("a").string
            event.url =  page_raw_event \
                .find("div", class_="notice-item-title").find("a").get("href")      
            event.address = page_raw_event \
                .find("div", class_="notice-item-top-location") \
                .find("p").string

            is_valid_event, event_additional_info = _get_event_additional_info(event.url)
            if not is_valid_event:
                continue

            event.description = event_additional_info["description"]
            for tag_type_name in event_additional_info["event_tags"]:
                event.tags.add(Tag.objects.get(tag_code=tag_types[tag_type_name]))
            
            event.type_of_event = EventTypeClissifier \
                .objects.get(type_code=event_types["Конференция"])

            # Проверка на актуальность
            if event.registration_deadline < datetime.now(tzlocal()).astimezone(moscow_tz):
                continue

            events.append(event)

    return events


# Ключ, необходимый для выполнения ajax запроса
def _get_nonce_key() -> str:
    response = requests.get("https://na-konferencii.ru/")
    html_decoded_string = html.unescape(response.text)
    soup = BeautifulSoup(html_decoded_string, "html.parser")

    script = soup.find("script", attrs={"id": "filter-js-extra"})
    nonce_key_name_index = script.string.index("\"nonce\"")
    script_content_shortened = script.string[nonce_key_name_index:]
    raw_nonce_key = script_content_shortened[
        script_content_shortened.index(":") + 1:
        script_content_shortened.index("}")
    ]
    nonce_key = raw_nonce_key.strip("\"")
    return nonce_key


def _get_event_additional_info(event_url) -> dict:
    result = {}

    response = requests.get(event_url)
    html_decoded_string = html.unescape(response.text)
    page = BeautifulSoup(html_decoded_string, "html.parser")

    description_paragraphs = page \
        .find("div", class_="content-page-body") \
        .find_all("p", recursive=False)
    description = ""
    alternative_description = page.find("meta", attrs={"name": "description"}).get("content")

    for paragraph in description_paragraphs:
        if paragraph.string is not None:
            description += f"\n{paragraph.string}"
    
    header = page.find("div", class_="content-page-header-inner")
    raw_tags = header.find_all("a")
    tags = [raw_tag.string for raw_tag in raw_tags]
    
    is_valid_event = False
    for category_name in categories.keys():
        if category_name in tags:
            is_valid_event = True

    event_tags = []

    for tag_type_name in tag_types.keys():
        if tag_type_name in tags:
            event_tags.append(tag_type_name)

    result["event_tags"] = event_tags

    result["description"] = description \
        if len(description) > len(alternative_description) \
        else alternative_description

    return (is_valid_event, result)
