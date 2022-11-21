import json

import re
from django.db.models import QuerySet
from main.models import Event, Tag
from app.settings import BASE_DIR


def update_all_v2(path: str, events: QuerySet, word_counter: int = 5):
    """
    метод для расстановки тегов
    :param path: путь до файла с тегами и ключевыми словами
    :param events: список элементов куда будут писаться  теги
    :param word_counter: количество слов нужных постановки тега
    :return: None
    """
    tags = {}
    with open(str(BASE_DIR) + path) as f:
        json_with_keys: dict = json.load(f)
        tags = json_with_keys["tags"]

    for event in events:
        text = event.description + " " + event.title
        clean_text = re.sub(r"[;,./?!'\"]", "", text.lower())

        for key, values in tags.items():
            counter = 0
            for word_for_check in values:
                founded_items = re.findall(word_for_check, clean_text)
                counter += len(founded_items)

            if counter >= word_counter:
                tag_for_event = Tag.objects.filter(description=key)
                event.tags.add(tag_for_event[0])
                event.save()


def all_events_tagger():
    """
    метод для растановки тегов для эвентов
    :return: None
    """
    path = '/main/data/data.json'
    events = Event.objects.all()
    update_all_v2(path=path, events=events, word_counter=1)
