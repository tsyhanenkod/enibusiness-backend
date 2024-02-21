from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer

from apps.users.models import CustomUser
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class SignupView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class SetPasswordView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


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
            # Do something with the validated data if needed
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
            
            # Return a response if everything is successful
            return Response({"user": user_data, "message": "Login successful"}, status=status.HTTP_200_OK)
        
        # If serializer is not valid, return an appropriate response
        return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            token_key = user.auth_token.key

            if Token.objects.filter(key=token_key).exists():
                # Если токен существует, удаляем его
                token = Token.objects.get(key=token_key)
                token.delete()
                return Response({'message': "Logout successfully!"}, status=status.HTTP_200_OK)
            else:
                # Если токена нет, возвращаем ошибку
                return Response({'error': "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class OtpVerificationView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class SetNewPasswordView(APIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)