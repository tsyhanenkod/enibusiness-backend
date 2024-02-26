from rest_framework import serializers
from .models import UserGroup
from apps.users.models import CustomUser

class GroupSerializer(serializers.ModelSerializer):
    usres = []
    class Meta:
        model = UserGroup
        fields = ['id', 'title', 'description', 'users']