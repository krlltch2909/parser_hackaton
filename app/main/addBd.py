from main.models import EventTypeClissifier, StatusOfEvent

# conference
# hackaton
# CTF
# olimpiada
# scientific publication


def add_event_type_to_bd():
    if len(EventTypeClissifier.objects.all()) == 0:
        EventTypeClissifier.objects.create(type_code=1, description='conference')
        EventTypeClissifier.objects.create(type_code=2, description='hackaton')
        EventTypeClissifier.objects.create(type_code=3, description='CTF')
        EventTypeClissifier.objects.create(type_code=4, description='olimpiada')
        EventTypeClissifier.objects.create(type_code=5, description='scientific publication')


def add_status_type_to_bd():
    if len(StatusOfEvent.objects.all()) == 0:
        StatusOfEvent.objects.create(status_code=1, description='in process')
        StatusOfEvent.objects.create(status_code=2, description='ended')
        StatusOfEvent.objects.create(status_code=3, description='unavailable')
        StatusOfEvent.objects.create(status_code=4, description='registration')
        StatusOfEvent.objects.create(status_code=5, description='scientific publication')

