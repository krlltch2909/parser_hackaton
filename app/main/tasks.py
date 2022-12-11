from datetime import datetime
from celery import shared_task
from .parsers.utils import clean_event
from .models import Event
from .parsers import *
from .tagger import all_events_tagger


@shared_task
def clean_database() -> None:
    saved_hackatons = Event.objects.all()
    count_if_deleted_events = 0
    for event in saved_hackatons:
        if event.is_expired():
            event.delete()
            count_if_deleted_events += 1

    print(f'ended, deleted {count_if_deleted_events} events')


@shared_task
def parse_new_events() -> None:
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
    return_rez: list[Event] = []
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
            
    for event in return_rez:
        clean_event(event)
        
    time_end = datetime.now() - time_start
    print(time_end)
    print(len(return_rez))

    for event in return_rez:
        try:
            if not event.already_exists():
                event.save()
        except Exception as e:
            print("error in saving " + str(e))
    all_events_tagger()
    print('ended')
