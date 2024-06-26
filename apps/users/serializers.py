from rest_framework import serializers
from apps.users.models import CustomUser, Referal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'location', 'phone_number', 'company_name', 'website', 'address', 'social_media', 'image', 'is_staff']
        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'location', 'phone_number']


class BusinessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Замените на вашу модель пользователя
        fields = ['company_name', 'website', 'address', 'social_media']
        
        
class ReferalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    refered_user = UserSerializer()
    class Meta:
        model = Referal
        fields = '__all__'
