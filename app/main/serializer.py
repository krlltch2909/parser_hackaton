from rest_framework import serializers
from .models import Title


class TitileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'
