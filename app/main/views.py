from django.shortcuts import render, HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event, EventTypeClissifier, StatusOfEvent
from .serializer import EventSerializer



# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
#
# import django
# django.setup()


# Create your views here.

class TitleAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


def test(request):



    # add_status_type_to_bd()
    return HttpResponse('<h1>sending</h1>')