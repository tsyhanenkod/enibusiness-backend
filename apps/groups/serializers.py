from rest_framework import serializers
from .models import UserGroup

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['id', 'title', 'description']