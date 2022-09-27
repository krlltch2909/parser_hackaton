from django.core.management.base import BaseCommand
from main.models import EventTypeClissifier, StatusOfEvent


class Command(BaseCommand):
    help = "Command for creating classifiers"

    def handle(self, *args, **options):
        if len(EventTypeClissifier.objects.all()) == 0:
            EventTypeClissifier.objects.create(type_code=1, description='conference')
            EventTypeClissifier.objects.create(type_code=2, description='hackathon')
            EventTypeClissifier.objects.create(type_code=3, description='CTF')
            EventTypeClissifier.objects.create(type_code=4, description='olimpiada')
            EventTypeClissifier.objects.create(type_code=5, description='scientific publication')
            EventTypeClissifier.objects.create(type_code=6, description='championship')

        if len(StatusOfEvent.objects.all()) == 0:
            StatusOfEvent.objects.create(status_code=1, description='in process')
            StatusOfEvent.objects.create(status_code=2, description='ended')
            StatusOfEvent.objects.create(status_code=3, description='unavailable')
            StatusOfEvent.objects.create(status_code=4, description='registration')
