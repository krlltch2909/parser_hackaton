from datetime import datetime
from celery import shared_task
from dateutil.relativedelta import relativedelta

from .models import Event
from .parsers.all_events import get_all_events
from .parsers.hackathon_com import get_hackathon_com_events
from .parsers.hacks_ai import get_hacks_ai_events
from .parsers.ict2go_events import get_ict2go_events
from .parsers.leader_id import get_leader_id_events
from .parsers.leaders_of_digital import get_leaders_of_digital_events
from .parsers.na_conferencii import get_na_conferencii_events
from .parsers.university_2035 import get_2035_university_events
from .tagger import all_events_tagger

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
    all_threads = [get_all_events,
                   get_hackathon_com_events,
                   get_hacks_ai_events,
                   get_ict2go_events,
                   get_leader_id_events,
                   get_leaders_of_digital_events,
                   get_na_conferencii_events,
                   get_2035_university_events
                   ]

    time_start = datetime.now()
    return_rez = []
    for task in all_threads:
        try:
            rez = task()
            print(task.__str__() + " - " + str(len(rez)))

            return_rez += rez
        except KeyError:
            print("Key error")
        except RuntimeError:
            print("Runtime error")
        except Exception as e:
            print("error " + str(e))
            print(e.args)

    time_end = datetime.now() - time_start
    print(time_end)
    print(len(return_rez))

    saved_events = Event.objects.all()
    for event in return_rez:
        try:
            find_same_event = saved_events.filter(title=event.title, start_date=event.start_date)

            if len(find_same_event) == 0:
                event.save()
            # else:
            #     for i in find_same_event:
            #         print(f"bd event {i.title} | found new event {event.title}")

        except Exception as e:
            print("error in saving " + str(e))
    # all_events_tagger()
    # conference_tagger()


    print('ended')
