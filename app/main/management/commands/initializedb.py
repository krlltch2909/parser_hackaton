from django.core.management.base import BaseCommand
from main.models import EventTypeClissifier, Tag


class Command(BaseCommand):
    help = "Command for creating classifiers"

    def handle(self, *args, **options):
        if len(EventTypeClissifier.objects.all()) == 0:
            EventTypeClissifier.objects.create(type_code=1, description='Конференция')
            EventTypeClissifier.objects.create(type_code=2, description='Хакатон')
            EventTypeClissifier.objects.create(type_code=3, description='Соревнование')
            EventTypeClissifier.objects.create(type_code=4, description='Акселератор')
            EventTypeClissifier.objects.create(type_code=5, description='Конкурс')

        if len(Tag.objects.all()) == 0:
            Tag.objects.create(tag_code=1, description="РИНЦ")
            Tag.objects.create(tag_code=2, description="Перечень ВАК")
            Tag.objects.create(tag_code=3, description="Scopus")
            Tag.objects.create(tag_code=4, description="Web of Science")

            Tag.objects.create(tag_code=5, description="Управление данными")
            Tag.objects.create(tag_code=6, description="Информационная безопасность")
            Tag.objects.create(tag_code=7, description="Машинное обучение")
            Tag.objects.create(tag_code=8, description="Искусственный интеллект")
            Tag.objects.create(tag_code=9, description="Виртуальная реальность")
            Tag.objects.create(tag_code=10, description="Дополненная реальность")
            Tag.objects.create(tag_code=11, description="Интернет вещей")
            Tag.objects.create(tag_code=12, description="Робототехника")