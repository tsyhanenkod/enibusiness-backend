from rest_framework import serializers
from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'location', 'phone_number', 'image', 'is_staff']
        

class BusinessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Замените на вашу модель пользователя
        fields = ['company_name', 'website', 'address', 'social_media']