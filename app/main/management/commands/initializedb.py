import json
from django.core.management.base import BaseCommand
from main.models import EventTypeClissifier, Tag


DATA_FILE = "main/data/data.json"


class Command(BaseCommand):
    help = "Command for creating classifiers"

    def handle(self, *args, **options):
        with open(DATA_FILE, "r") as file:
            data: dict = json.load(file) 
            if len(EventTypeClissifier.objects.all()) == 0:  
                for event_type in data["types"]:
                    EventTypeClissifier.objects.create(description=event_type)

            if len(Tag.objects.all()) == 0:
                tags: list = data["tags"].keys()
                for tag in tags:
                    Tag.objects.create(description=tag)
