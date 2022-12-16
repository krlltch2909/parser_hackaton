import re
from main.models import *


HTML_TAG_CLEANER = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def get_event_types() -> dict[str, int]:
    event_types: dict[str, int] = {}
    for event_type in EventTypeClissifier.objects.all():
        event_types[event_type.description] = event_type.type_code
    return event_types


def get_tag_types() -> dict[str, int]:
    tag_types: dict[str, int] = {}
    for tag_type in Tag.objects.all():
        tag_types[tag_type.description] = tag_type.tag_code
    return tag_types


def clean_event(event: Event) -> None:    
    clean_event_title(event)
    event.description = re.sub(HTML_TAG_CLEANER, "", event.description)
    if event.address is not None:
        event.address = re.sub(HTML_TAG_CLEANER, "", event.address)


def clean_event_title(event: Event) -> None:
    event.title = re.sub(HTML_TAG_CLEANER, "", event.title)
    splitted_title = event.title.split(" ")
    result_parts = []
    for title_part in splitted_title:
        if "#" not in title_part:
            result_parts.append(title_part)    
    event.title = " ".join(result_parts)
