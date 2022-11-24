import re
from main.models import *

# Регулярное выражение, позволяющее очищать текст от html-тегов
CLEANER = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


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
    event.title = re.sub(CLEANER, "", event.title)
    event.description = re.sub(CLEANER, "", event.description)
    
    if event.address is not None:
        event.address = re.sub(CLEANER, "", event.address)
