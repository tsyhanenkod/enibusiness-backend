from rest_framework import serializers
from apps.users.models import CustomUser
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    class Meta:
        fields = ["email", "password"]
        
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exist")
        else: 
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                return attrs
            else:
                raise serializers.ValidationError("Wrong password")
        
        