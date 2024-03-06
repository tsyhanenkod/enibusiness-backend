from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import CustomUser, Referal
from .serializers import UserSerializer, BusinessDataSerializer, ReferalSerializer, UserUpdateSerializer


class GetUsersView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request):
        serializer = self.serializer_class(CustomUser.objects.all(), many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No users found'}, status=status.HTTP_404_NOT_FOUND)

class EditUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if not request.data.get('email'):
            return Response({'error': 'Email can\'t be empty'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not request.data.get('first_name'):
            return Response({'error': 'Email can\'t be empty'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        user = get_object_or_404(CustomUser, email=request.user.email)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data, "message": "User data updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class EditBusinessDataView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BusinessDataSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data, 'message': 'Business data updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        


class ProfileImageView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.image:
            return Response({'error': 'Profile image not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'image': user.image.url}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, email=request.user.email)
        profile_image = request.FILES.get('image')
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not profile_image:
            return Response({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if request.user.image:
                old_image_path = request.user.image.path
                default_storage.delete(old_image_path)
            if profile_image:
                user.image = profile_image
                user.save()
            return Response({"image": user.image.url, 'message': 'Profile image updated successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to update profile image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            if not user.image.path:
                return Response({'error': 'Profile image not found'}, status=status.HTTP_404_NOT_FOUND)
            default_storage.delete(user.image.path)
            user.image = None
            user.save()
            return Response({'message': 'Profile image deleted successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to delete profile image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_staff:
            return Response({'error': 'Admin can\'t delete account'}, status=status.HTTP_403_FORBIDDEN)
        if not request.data.get('email'):
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not CustomUser.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        try: 
            user = get_object_or_404(CustomUser, email=request.data.get('email'))
            if user.image:
                default_storage.delete(user.image.path)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
# referals
class GetReferalsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReferalSerializer
    
    def get(self, request):
        user = request.user
        referals = Referal.objects.filter(user=user)
        serializer = self.serializer_class(referals, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No referals found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        to_user_email = request.data.get('to_user')
        project = request.data.get('project')
        amount = request.data.get('amount')

        to_user = CustomUser.objects.filter(email=to_user_email).first()

        if not to_user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'user': user.id,
            'refered_user': to_user.id,
            'project': project,
            'amount': amount,
        }

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            saved_referal = Referal.objects.get(id=serializer.data['id'])

            return Response({
                "referal": self.serializer_class(saved_referal).data,
                "message": "Referral added successfully"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        user = request.user
        referal_id = request.data.get('id')
        referal = Referal.objects.filter(user=user, id=referal_id).first()
        if not referal:
            return Response({'error': 'Referal not found'}, status=status.HTTP_404_NOT_FOUND)
        referal.delete()
        return Response({'message': 'Referal deleted successfully'}, status=status.HTTP_200_OK)
    
    
    
class GetReceivedReferalsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReferalSerializer
    
    def get(self, request):
        user = request.user
        referals = Referal.objects.filter(refered_user=user)
        serializer = self.serializer_class(referals, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No referals found'}, status=status.HTTP_404_NOT_FOUND)
    
