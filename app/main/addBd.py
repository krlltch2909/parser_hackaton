from main.models import EventTypeClissifier, StatusOfEvent

# conference
# hackaton
# CTF
# olimpiada
# scientific publication


def add_event_type_to_bd():
    if all(EventTypeClissifier.objects.all()) == 0:
        EventTypeClissifier.objects.create(type_code=1, description='conference')
        EventTypeClissifier.objects.create(type_code=2, description='hackaton')
        EventTypeClissifier.objects.create(type_code=3, description='CTF')
        EventTypeClissifier.objects.create(type_code=4, description='olimpiada')
        EventTypeClissifier.objects.create(type_code=5, description='scientific publication')
        EventTypeClissifier.save()


def add_status_type_to_bd():
    if all(StatusOfEvent.objects.all()) == 0:
        StatusOfEvent.objects.create(type_code=1, description='in process')
        StatusOfEvent.objects.create(type_code=2, description='ended')
        StatusOfEvent.objects.create(type_code=3, description='unavailable')
        # StatusOfEvent.objects.create(type_code=4, description='registration')
        # StatusOfEvent.objects.create(type_code=5, description='scientific publication')
        StatusOfEvent.save()

if __name__ == '__main__':
    add_event_type_to_bd()