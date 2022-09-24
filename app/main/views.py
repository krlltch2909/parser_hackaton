from django.shortcuts import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializer import EventSerializer


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
        return queryset


def test(request):
    # add_status_type_to_bd()
    return HttpResponse('<h1>sending</h1>')
