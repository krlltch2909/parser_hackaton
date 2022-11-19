from rest_framework import serializers
from .models import Event, Tag, EventTypeClissifier


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypeClissifier
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    type_of_event = EventTypeSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
