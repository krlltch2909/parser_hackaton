import json
from django.core.management.base import BaseCommand
from main.models import EventTypeClissifier, Tag, Keyword


DATA_FILE = "main/data/init.json"


class Command(BaseCommand):
    help = "Command for creating classifiers"

    def handle(self, *args, **options):
        with open(DATA_FILE, "r") as file:
            data: dict = json.load(file) 
            for event_type in data["types"]:
                exists = EventTypeClissifier.objects.filter(description=event_type)\
                    .exists()
                if not exists:
                    EventTypeClissifier.objects.create(description=event_type)

            tags: dict = data["tags"]
            for tag_name, keywords in tags.items():
                exists = Tag.objects.filter(description=tag_name)\
                    .exists()                
                if not exists:
                    Tag.objects.create(description=tag_name)
                    new_tag = Tag.objects.get(description=tag_name)
                    for keyword in keywords:
                        Keyword.objects.create(content=keyword, tag_code=new_tag)                        
