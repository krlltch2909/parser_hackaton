from datetime import datetime
from fonetika.soundex import RussianSoundex
from main.models import Event
from app.settings import BASE_DIR

import json
soundex = RussianSoundex(cut_result=True, seq_cutted_len=4, code_vowels=True)


def snd_match(l: list, a: str) -> list:
    snd_heap = [(soundex.transform(x), x) for x in l]
    return [x[1] for x in snd_heap if (soundex.transform(a)[:len(a) + 1] in x[0])]


def update_all():
    with open(str(BASE_DIR) + '/main/parsers/keywords.json') as f:
        keys: dict = json.load(f)

    time_start = datetime.now()
    rez_events = []
    events = Event.objects.all()
    keys_wth_codes = {}

    for json_string in keys:
        keys_wth_codes[json_string] = []
        for i in keys.get(json_string):
            snd_heap = soundex.transform(i)
            keys_wth_codes.get(json_string).append(snd_heap)

    event_dict = {}

    for event in events:
        text = event.description
        text = text.split(' ')

        # новый варик меньше одной секуды
        # rez = 0

        event_tags = {}
        # print(keys)
        for key_for_keys in keys:
            event_tags[key_for_keys] = 0

        for word in text:
            word = (soundex.transform(word), word)
            for keys_for_word in keys_wth_codes:
                for i in keys_wth_codes.get(keys_for_word):
                    if i[:len(i) + 1] in word[0]:
                        event_tags[keys_for_word] += 1

        for i in event_tags:
            if event_tags.get(i) >= 5:
                rez_events.append(event)
                event_dict[event.title] = i

        # старый варик 5 секунд
        # for i in keys.get('Big Data'):
        #     try:
        #         len_of_find_words = len(snd_match(text, i))
        #         if len_of_find_words > 1:
        #             rez.append(len_of_find_words)
        #     except Exception:
        #         print('ERROR')

        # print(rez)

    print(event_dict)
    time_end = datetime.now() - time_start

    print("time of working - " + str(time_end))


