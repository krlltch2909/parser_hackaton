from celery import shared_task
from .parsers.leaders_of_digital import get_leaders_of_digital_events
from .parsers.hacks_ai import get_hacks_ai_events
from .models import Event


@shared_task
def clean_data_base():
    """
    method for cleaning database from outdated events
    :return: None
    """
    pass


@shared_task
def parse_new_events():
    """
    method for parsing sites
    :return:
    """
    rez1 = get_hacks_ai_events()
    rez2 = get_leaders_of_digital_events()
    return_rez = rez1 + rez2
    for event in return_rez:
        event.save()
