import re
from django.db.models import QuerySet
from main.models import Event, Tag, Keyword


def update_all_v2(events: QuerySet, word_counter: int = 5) -> None:
    """
    метод для расстановки тегов
    :param events: список элементов, которым будут присваиваться теги
    :param word_counter: кол-во совпадений слов, необходимое для присваивания тега
    :return: None
    """
    tags = Tag.objects.all()

    for event in events:
        text = event.description + " " + event.title
        clean_text = re.sub(r"[;,./?!'\"]", "", text.lower())

        for tag in tags:
            tag_keywords = Keyword.objects.filter(tag_code=tag.tag_code)
            counter = 0
            
            for keyword in tag_keywords:
                founded_items = re.findall(keyword.content, clean_text)
                counter += len(founded_items)

            if counter >= word_counter:
                event.tags.add(tag)
                event.save()


def all_events_tagger() -> None:
    """
    метод для растановки тегов для ивентов
    :return: None
    """
    events = Event.objects.all()
    update_all_v2(events=events, word_counter=1)
