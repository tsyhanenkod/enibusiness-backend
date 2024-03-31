from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.groups.models import UserGroup

from .serializers import (
    LoginSerializer, 
    ForgotPasswordSerializer, 
    OtpVerificationSerializer, 
    SetNewPassSerializer, 
    SignupSerializer, 
    RequestedUserSerializer,
    RequestSignupSerializer
)

from apps.users.models import CustomUser, TemporaryUser, RequestedUser
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from .utils import (
    register_mail, 
    otp_code_mail, 
    generateOtp,
    request_signup_success,
    request_signup_admin_nitification,
    request_signup_rejected,
)

import secrets
import base64


class SignupRequestView(APIView):
    serializer_class = RequestedUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = RequestedUser.objects.create(
                    **serializer.validated_data
                )

                request_signup_admin_nitification(user.email, user.first_name, user.last_name, user.phone, user.location, user.business)

                return Response({"message": "Request sent successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)


class SignupAcceptRequestView(APIView):
    serializer_class = RequestSignupSerializer
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            users = RequestedUser.objects.all()
            user_list = list(users.values())

            return Response({
                "data": user_list, 
                "message": "Request sent successfully"
            }, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)

    
    def post(self, request):
        try:
            req_user_email = request.data.get('email')
            req_user = RequestedUser.objects.get(email=req_user_email)

            token = secrets.token_urlsafe()
            encoded_token = base64.b64encode(token.encode()).decode()
            
            temp_user = TemporaryUser.objects.create(
                token=token,
                first_name=req_user.first_name,
                last_name=req_user.last_name,
                email=req_user.email,
                location=req_user.location,
                phone=req_user.phone
            )

            request_signup_success(temp_user.email, encoded_token)

            req_user.delete()

            return Response({"message": "Request user accepted successfully"}, status=status.HTTP_200_OK)
        except RequestedUser.DoesNotExist:
            return Response({"error": "Requested user does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            user_id = request.data.get('id')
            user = RequestedUser.objects.get(id=user_id)
            
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

            request_signup_rejected(user.email)
            user.delete()

            return Response({"message": "Request user refected successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)



class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                token = secrets.token_urlsafe()
                encoded_token = base64.b64encode(token.encode()).decode()
                
                user = TemporaryUser.objects.create(
                    token=token,
                    **serializer.validated_data
                )
                
                register_mail(user.email, encoded_token)

                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            except:
                return Response({"error": "Invalid data provided"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        


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
                user = CustomUser.objects.create_user(
                    email=temp_user.email,
                    first_name=temp_user.first_name,
                    last_name=temp_user.last_name,
                    password=password,
                    location=temp_user.location,
                    phone_number=temp_user.phone
                )

                if temp_user.group:
                    group = UserGroup.objects.get(id=temp_user.group)
                    group.users.add(user.id)

                temp_user.delete()

                return Response({"message": "Password set successfuly"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):    
    serializer_class = LoginSerializer
    
    def post(self, request):
        if request.data.get("email") is None or request.data.get("email") == "":
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("password") is None or request.data.get("password") == "":
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(request.data.get('password')) < 8:
            return Response({"error": "Password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)
        if not CustomUser.objects.filter(email=request.data.get("email")).exists():
            return Response({"error": "User with this email dosen't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)            
        if serializer.is_valid(raise_exception=True):

            email = serializer.validated_data.get("email")
            user = CustomUser.objects.get(email=email)
            
            try:
                user = authenticate(email=email, password=serializer.validated_data.get("password"))
                
                if user is None:
                    return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
                else:           
                    token, created = Token.objects.get_or_create(user=user)
                    if user.image:
                        image = user.image.url
                    else: 
                        image = ''
                
                    user_data = {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "location": user.location,
                        "phone_number": user.phone_number,
                        "image": image,
                        "groups": user.groups.all(),
                        "company_name": user.company_name,
                        "website": user.website,
                        "address": user.address,
                        "social_media": user.social_media,
                        "token": token.key,
                        "is_admin": user.is_staff,
                    }
                    
                    return Response({"user": user_data, "message": "Login successful"}, status=status.HTTP_200_OK) 
            except:
                return Response({"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"message": serializer.errors.get('non_field_errors')[0]}, status=status.HTTP_400_BAD_REQUEST)
        
        
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
                
                # request.session['reset_email'] = email
                
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