from rest_framework import serializers
from .models import UserGroup
from apps.users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    usres = []
    class Meta:
        model = UserGroup
        fields = ['id', 'title', 'description', 'users']


class MyEniUsersSerialixer(serializers.ModelSerializer):
    users = CustomUserSerializer(many=True)
    
    class Meta:
        model = UserGroup
        fields = ['id', 'title', 'description', 'users']