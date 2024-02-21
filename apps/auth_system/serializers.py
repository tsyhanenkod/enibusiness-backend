from rest_framework import serializers
from apps.users.models import CustomUser
from django.contrib.auth import authenticate


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    location = serializers.CharField()
    phone = serializers.CharField()
    
    class Meta:
        fields = ["first_name", "last_name", "email", "location", "phone"]
        
    def validate(self, attrs):
        first_name = attrs.get("first_name")        
        last_name = attrs.get("last_name")
        email = attrs.get("email")
        location = attrs.get("location")
        phone = attrs.get("phone")
        
        return attrs


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
            

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ["email"]
    
    def validate(self, attrs):
        email = attrs.get("email")
        
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exist")
        
        return attrs
    

class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    
    class Meta:
        fields = ["email", "code"]
    
    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exist")
        
        if code is None or code == "":
            raise serializers.ValidationError("Code is required")
        
        return attrs
    
    
class SetNewPassSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ["email", "password", "confirm_password"]
    
    def validate(self, attrs):
        email = attrs.get("email")
                
        return attrs
        
        