from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event, Tag, EventTypeClissifier
from .serializer import EventSerializer, TagSerializer, EventTypeSerializer


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

        type_of_event_get = self.request.query_params.getlist('type_of_event')
        tags = self.request.query_params.getlist('tags')
        rez = []
        for type_event in type_of_event_get:
            if len(tags) > 0:
                for i in tags:
                    half_rez = Event.objects.filter(tags__tag_code=int(i))
                    if len(rez) == 0:
                        rez = half_rez
                    else:
                        rez = rez.union(half_rez)
            else:
                half_rez = Event.objects.filter(type_of_event=int(type_event))
                if len(rez) == 0:
                    rez = half_rez
                else:
                    rez = rez.union(half_rez)
        return rez


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
