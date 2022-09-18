from django.shortcuts import render
from rest_framework import generics
from .models import Title
from .serializer import TitileSerializer


# Create your views here.

class TitleAPIView(generics.ListAPIView):
    queryset = Title.objects.all()
    serializer_class = TitileSerializer
