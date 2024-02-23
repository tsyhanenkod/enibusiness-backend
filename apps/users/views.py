from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import CustomUser
from .serializers import UserSerializer


class GetUsersView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'This service only for admin users'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(CustomUser.objects.all(), many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No users found'}, status=status.HTTP_404_NOT_FOUND)

class EditUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.user.email)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if CustomUser.objects.filter(email=request.data.get('email')).exclude(email=request.user.email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_409_CONFLICT)
        
        try:
            user.first_name = request.data.get('first_name')
            user.last_name = request.data.get('last_name')
            user.email = request.data.get('email')
            user.location = request.data.get('location')
            user.phone_number = request.data.get('phone_number')
            user.save()
        
            user = {
                "image": user.image.url,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "location": user.location,
                "phone_number": user.phone_number,
                "is_staff": user.is_staff
            }
        
            return Response({"user": user, "message": "User data updated successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to update user data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.user.email)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(request.data.get('old_password')):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get('new_password') != request.data.get('new_password2'):
            return Response({'error': 'New passwords don\'t match'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user.set_password(request.data.get('new_password'))
            user.save()
            token_key = user.auth_token.key
            Token.objects.get(key=token_key).delete()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, 'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to change password'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class DeleteUserView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
