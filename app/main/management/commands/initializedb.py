from django.core.management.base import BaseCommand
from main.models import EventCostClassifier, EventTypeClissifier, Tags



class Command(BaseCommand):
    help = "Command for creating classifiers"

    def handle(self, *args, **options):
        if len(EventTypeClissifier.objects.all()) == 0:
            EventTypeClissifier.objects.create(type_code=1, description='Конференция')
            EventTypeClissifier.objects.create(type_code=2, description='Хакатон')
            EventTypeClissifier.objects.create(type_code=3, description='Соревнование')
            EventTypeClissifier.objects.create(type_code=4, description='Акселератор')
            EventTypeClissifier.objects.create(type_code=5, description='Конкурс')

        if len(Tags.objects.all()) == 0:
            Tags.objects.create(tage_code=1, description="Big Data")
            Tags.objects.create(tage_code=2, description="Информационная безопвсность")
