from rest_framework import serializers
from apps.users.models import CustomUser, TemporaryUser, RequestedUser
from django.contrib.auth import authenticate


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryUser
        fields = ['first_name', 'last_name', 'email', 'group', 'location', 'phone']
        extra_kwargs = {
            'last_name': {'required': False},
            'location': {'required': False},
            'group': {'required': False},
            'phone': {'required': False},
        }


class RequestSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryUser
        fields = '__all__'
        exclude = ['business']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    class Meta:
        fields = ["email", "password"]
        
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        return attrs
            

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        fields = ["email"]
    
    def validate(self, attrs):
        email = attrs.get("email")
                
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


class RequestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedUser
        fields = '__all__'
        
        