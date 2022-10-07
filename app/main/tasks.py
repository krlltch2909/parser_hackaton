from datetime import datetime
from celery import shared_task
from dateutil.relativedelta import relativedelta

from .models import Event
from .parsers.leaders_of_digital import get_leaders_of_digital_events
from .parsers.hacks_ai import get_hacks_ai_events
from .parsers.all_events import get_all_events
from .parsers.hackathon_com import get_hackathon_com_events


@shared_task
def clean_data_base() -> None:
    """
    method for cleaning database from outdated events
    :return: None
    """
    saved_hackatons = Event.objects.all()
    count_if_deleted_events = 0
    for event in saved_hackatons:
        if event.end_date is not None:
            if event.end_date <= datetime.now() - relativedelta(months=3):
                event.delete()
                count_if_deleted_events += 1

    print(f'ended, deleted {count_if_deleted_events} events')


@shared_task
def parse_new_events() -> None:
    """
    method for parsing and filtering sites
    :return: None
    """
    all_threads = [get_hacks_ai_events,
                   get_leaders_of_digital_events,
                   get_all_events,
                   get_hackathon_com_events]

    time_start = datetime.now()
    return_rez = []
    for tasks in all_threads:
        try:
            rez = tasks()
            print(len(rez))
            return_rez += rez
        except RuntimeError:
            print("error")
    time_end = datetime.now() - time_start
    print(time_end)
    print(len(return_rez))

    saved_events = Event.objects.all()

    for event in return_rez:
        find_same_event = saved_events.filter(title=event.title, start_date=event.start_date)
        print(find_same_event)
        if len(find_same_event) == 0:
            event.save()
        else:
            print("already exists")
    print('ended')
