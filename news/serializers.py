from rest_framework import serializers
from .models import Story


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['headline', 'category', 'region', 'details']
