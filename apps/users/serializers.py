from rest_framework import serializers
from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'location', 'phone_number', 'image', 'is_staff']
        
    