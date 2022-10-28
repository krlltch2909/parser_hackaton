from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event, Tag, EventTypeClissifier
from .serializer import EventSerializer, TagSerializer, EventTypeSerializer
from django.db.models.query import QuerySet

def filter_by_type(types: list, events_for_filtering: QuerySet) -> QuerySet:
    """
    метод для фильтрации мероприятий по типу (конференция, хакатон, итд)
    :param types: список с типами которые надо получить
    :param events_for_filtering:  список мероприятий для фильтрации
    :return: отфилтрованный по типам QuerySet или пустой список так ка совпадений не было
    """
    rez = []
    for type_of_event in types:
        half_rez = events_for_filtering.filter(type_of_event=int(type_of_event))
        if len(rez) == 0:
            rez = half_rez
        else:
            rez = rez.union(half_rez)
    return rez


def filter_by_tag(tags: list, events_for_filtering: QuerySet) -> QuerySet:
    """
     метод для фильтрации мероприятий по тегу (Искусственный интеллект, Управление данными, итд)
     :param tags: список с тегами которые надо получить
     :param events_for_filtering:  список мероприятий для фильтрации
     :return: отфилтрованный по типам QuerySet или пустой список так как совпадений не было
     """
    rez = []
    for i in tags:
        half_rez = events_for_filtering.filter(tags__tag_code=int(i))
        if len(rez) == 0:
            rez = half_rez
        else:
            rez = rez.union(half_rez)
    return rez


class TypeTitleAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EventSerializer
    

    def get_queryset(self):
        """
        апи для мерорпиятий
        параметры фильтрации:
            тег: один или много => tags
            тип события: один или много => type_of_event
        критерии для фильтрации передаются в запросе как параметры
        """
        all_events = Event.objects.all()
        type_of_event_get = self.request.query_params.getlist('type_of_event')
        tags = self.request.query_params.getlist('tags')

        if len(type_of_event_get) != 0:
            rez = filter_by_type(types=type_of_event_get, events_for_filtering=all_events)
            if len(tags) != 0:
                rez = filter_by_tag(tags=tags, events_for_filtering=rez)
        else:
            rez = filter_by_tag(tags=tags, events_for_filtering=all_events)

        if len(type_of_event_get) == 0 and len(tags) == 0:
            rez = all_events
        return rez.order_by('start_date')


class TagAPIView(generics.ListAPIView):
    """
    апи для всех тегов, фильтроции нет
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EventTypeAPIView(generics.ListAPIView):
    """
    апи для всех типов, фильтроции нет
    """
    permission_classes = [IsAuthenticated, ]
    queryset = EventTypeClissifier.objects.all()
    serializer_class = EventTypeSerializer
