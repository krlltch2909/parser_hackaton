import json
from django.core.management.base import BaseCommand
from main.models import EventTypeClissifier, Tag


DATA_FILE = "main/data/data.json"


class Command(BaseCommand):
    help = "Command for creating classifiers"

    def handle(self, *args, **options):
        with open(DATA_FILE, "r") as file:
            data: dict = json.load(file) 
            for event_type in data["types"]:
                print("before")
                exists = EventTypeClissifier.objects.filter(description=event_type)\
                    .exists()
                print("after")
                if not exists:
                    EventTypeClissifier.objects.create(description=event_type)

            tags: list = data["tags"].keys()
            for tag in tags:
                exists = Tag.objects.filter(description=tag)\
                    .exists()                
                if not exists:
                    Tag.objects.create(description=tag)
