from celery import shared_task
from .parsers.leaders_of_digital import get_leaders_of_digital_events
from .parsers.hacks_ai import get_hacks_ai_events
from .parsers.all_events import get_all_events
from .parsers.hackathon_com import get_hackathon_com_events
from .models import Event


@shared_task
def clean_data_base() -> None:
    """
    method for cleaning database from outdated events
    :return: None
    """
    pass


@shared_task
def parse_new_events() -> None:
    """
    method for parsing and filtering sites
    :return: None
    """
    rez1 = get_hacks_ai_events()
    rez2 = get_leaders_of_digital_events()
    rez3 = get_all_events()
    rez4 = get_hackathon_com_events()
    return_rez = rez1 + rez2 + rez3 + rez4

    saved_events = Event.objects.all()

    for event in return_rez:

        find_same_event = saved_events.filter(title=event.title, start_date=event.start_date)
        print(find_same_event)
        if len(find_same_event) == 0:
            event.save()
        else:
            print("already exists")
    print('ended')
