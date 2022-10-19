from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event, Tag
from .serializer import EventSerializer, TagSerializer


class TypeTitleAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EventSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned events to a given user,
        by filtering against a `type_of_event` query parameter in the URL.
        """
        queryset = Event.objects.all()

        type_of_event_get = self.request.query_params.get('type_of_event')
        if type_of_event_get is not None:
            queryset = queryset.filter(type_of_event=type_of_event_get)


        tags = self.request.query_params.getlist('tags')
        print(tags)
        if len(tags) > 0:
            return_rez = queryset.filter(tags__tag_code=int(tags[0]))
            tags.pop(0)
            for i in tags:
                return_rez = return_rez.union(queryset.filter(tags__tag_code=int(i)))
            return return_rez
        return queryset


class TagPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
