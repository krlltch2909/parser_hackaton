from rest_framework import serializers
from .models import Event, Tag, EventTypeClissifier


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypeClissifier
        fields = '__all__'
