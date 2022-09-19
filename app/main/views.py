from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializer import EventSerializer


# Create your views here.

class TitleAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
