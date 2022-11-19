import json

import re
from datetime import datetime
from django.db.models import F, Count, QuerySet
# from fonetika.soundex import RussianSoundex
from main.models import Event, Tag
from app.settings import BASE_DIR


# soundex = RussianSoundex(cut_result=True, seq_cutted_len=4, code_vowels=True)

#
# def update_all(path: str, events: QuerySet, word_counter: int = 5):
#     """
#     метод для расстановки тегов
#     :param path: путь до файла с тегами и ключевыми словами
#     :param events: список элементов куда будут писаться  теги
#     :param word_counter: количество слов нужных постановки тега
#     :return: None
#     """
#     with open(str(BASE_DIR) + path) as f:
#         keys: dict = json.load(f)
#
#     time_start = datetime.now()
#     rez_events = []
#     keys_wth_codes = {}
#
#     for json_string in keys:
#         keys_wth_codes[json_string] = []
#         for i in keys.get(json_string):
#             snd_heap = soundex.transform(i)
#             keys_wth_codes.get(json_string).append(snd_heap)
#
#     event_dict = {}
#     counter = 0
#     for event in events:
#         if len(event.tags.all()) == 0:
#             text = event.description + " " + event.title
#             text = text.split(' ')
#             event_tags = {}
#             for key_for_keys in keys:
#                 event_tags[key_for_keys] = 0
#
#             for word in text:
#                 try:
#                     if len(word) != 0:
#                         word = (soundex.transform(word), word)
#                         for keys_for_word in keys_wth_codes:
#                             for i in keys_wth_codes.get(keys_for_word):
#                                 if i[:len(i) + 1] in word[0]:
#                                     event_tags[keys_for_word] += 1
#                 except:
#                     print("errror in " + str(word))
#
#             for i in event_tags:
#                 if event_tags.get(i) >= word_counter:
#                     tag_for_event = Tag.objects.filter(description=i)
#
#                     if len(tag_for_event) > 0:
#                         event.tags.add(tag_for_event[0])
#                         event.save()
#                         counter += 1
#                         rez_events.append(event)
#                         event_dict[event.title] = i
#
#     print(event_dict)
#     time_end = datetime.now() - time_start
#     print("time of working - " + str(time_end))
#     print(counter)

def update_all_v2(path: str, events: QuerySet, word_counter: int = 5):
    """
    метод для расстановки тегов
    :param path: путь до файла с тегами и ключевыми словами
    :param events: список элементов куда будут писаться  теги
    :param word_counter: количество слов нужных постановки тега
    :return: None
    """
    with open(str(BASE_DIR) + path) as f:
        json_with_keys: dict = json.load(f)

    count_of_tegged_events = 0
    for event in events:
        # if len(event.tags.all()) == 0:
        text = event.description + " " + event.title
        clean_text = re.sub(r"[;,./?!'\"]", "", text.lower())

        for key, values in json_with_keys.items():
            counter = 0
            for word_for_check in values:
                founded_items = re.findall(word_for_check, clean_text)
                counter += len(founded_items)

            if counter > word_counter:
                tag_for_event = Tag.objects.filter(description=key)
                event.tags.add(tag_for_event[0])
                event.save()
                count_of_tegged_events += 1
                print(event, event.tags.all(), sep=" | ")
    print(count_of_tegged_events)


# def conference_tagger():
#     """
#     метод для расстановки тегов для конференцей
#     :return:None
#     """
#     path = '/main/parsers/keys/conference_tag.json'
#     events = Event.objects.filter(type_of_event=1)
#     update_all(path=path, events=events, word_counter=1)
#

def all_events_tagger():
    """
    метод для растановки тегов для эвентов
    :return: None
    """
    path = '/main/parsers/keys/keywords.json'
    events = Event.objects.all()
    update_all_v2(path=path, events=events, word_counter=3)
