from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer, ForgotPasswordSerializer, OtpVerificationSerializer, SetNewPassSerializer, SignupSerializer

from apps.users.models import CustomUser, TemporaryUser
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from .utils import register_mail, otp_code_mail, generateOtp

import secrets
import base64


class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        location = request.data.get('location')
        phone = request.data.get('phone')
        
        if not first_name or first_name == '':
            return Response({"error": "First name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not last_name or last_name == '':
            return Response({"error": "Last name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not email or email == '':
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not location or location == '':
            return Response({"error": "Location is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not phone or phone == '':
            return Response({"error": "Phone is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if TemporaryUser.objects.filter(email=email).exists():
            return Response({"error": "User with this email already created by admin"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                token = secrets.token_urlsafe()
                encoded_token = base64.b64encode(token.encode()).decode()
                
                user = TemporaryUser.objects.create(
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    location=location, 
                    phone=phone, 
                    token=token
                )
                user.save()
                
                register_mail(email, encoded_token)

                return Response({"message": "User created successfuly"}, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Invalid data provided"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        


class SetPasswordView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        token = self.kwargs.get('token')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        decoded_token = base64.b64decode(token).decode()
        
        try:
            temp_user = TemporaryUser.objects.get(token=decoded_token)
            if password != password2:
                return Response({"error": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                CustomUser.objects.create_user(
                    email=temp_user.email,
                    first_name=temp_user.first_name,
                    last_name=temp_user.last_name,
                    password=password,
                    location=temp_user.location,
                    phone_number=temp_user.phone
                )

                temp_user.delete()
                return Response({"message": "Password set successfuly"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):    
    serializer_class = LoginSerializer
    
    def post(self, request):
        if request.data.get("email") is None or request.data.get("email") == "":
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("password") is None or request.data.get("password") == "":
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(request.data.get('password')) < 8:
            return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)            
        if serializer.is_valid(raise_exception=True):

            email = serializer.validated_data.get("email")
            user = CustomUser.objects.get(email=email)
            
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "location": user.location,
                "phone_number": user.phone_number,
                "image": user.image.url if user.image else None,
                "token": token.key
            }
            
            return Response({"user": user_data, "message": "Login successful"}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            token_key = user.auth_token.key

            if Token.objects.filter(key=token_key).exists():

                token = Token.objects.get(key=token_key)
                token.delete()
                return Response({'message': "Logout successfully!"}, status=status.HTTP_200_OK)
            else:

                return Response({'error': "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    
    def post(self, request):
        email = request.data.get("email")
        if email is None or email == "":
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not CustomUser.objects.filter(email=email).exists():
            return Response({"error": "User with this email dosen't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = CustomUser.objects.get(email=email)
                user.reset_code = generateOtp()
                user.save()
                otp_code_mail(email, user.reset_code)
                
                request.session['reset_email'] = email
                
                return Response({"message": "Code sent to email successfuly"}, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OtpVerificationView(APIView):
    serializer_class = OtpVerificationSerializer
    
    def post(self, request):
        if request.data.get("code") is None or request.data.get("code") == "":
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = CustomUser.objects.get(email=request.data.get('email'))
            if user.reset_code != request.data.get("code"):
                return Response({"error": "Code is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Verified successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    serializer_class = SetNewPassSerializer
    def post(self, request):
        if request.data.get("password") is None or request.data.get("password") == "":
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(request.data.get('password')) < 8:
            return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("password2") is None or request.data.get("password") == "":
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(request.data.get('password2')) < 8:
            return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("password") != request.data.get("password2"):
            return Response({"error": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = request.data.get("email")
            user = CustomUser.objects.get(email=email)
            user.set_password(request.data.get("password"))
            user.save()
            return Response({"message": "Password changed successfuly"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something go wrong"}, status=status.HTTP_400_BAD_REQUEST)