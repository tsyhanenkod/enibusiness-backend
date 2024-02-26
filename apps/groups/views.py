from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import UserGroup
from .serializers import GroupSerializer

from django.db import IntegrityError
from django.shortcuts import get_object_or_404


class GetAllGroupsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'This service only for admin users'}, status=status.HTTP_403_FORBIDDEN)

        groups = UserGroup.objects.all()
        serialized_groups = self.serializer_class(groups, many=True).data
        
        return Response({"groups": serialized_groups}, status=status.HTTP_200_OK)
    
    
class GetGroupView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    def get(self, request, id):
        if not request.user.is_staff:
            return Response({'error': 'This service only for admin users'}, status=status.HTTP_403_FORBIDDEN)
        group = UserGroup.objects.filter(id=id)
        serialized_group = self.serializer_class(group, many=True).data
        
        return Response({"groups": serialized_group}, status=status.HTTP_200_OK)
    
    
class CreateGroupView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        
        if not request.user.is_staff:
            return Response({'error': 'This service only for admin users'}, status=status.HTTP_403_FORBIDDEN)
        if not title:
            return Response({'error': 'Group title is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not description:
            return Response({'error': 'Group description is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            serialized_group = self.serializer_class(group).data
            return Response({'group': serialized_group, 'message': 'Group created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create group'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class EditGroupView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    
    def put(self, request):
        if not request.user.is_staff:
            return Response({'error': 'This service is only for admin users'}, status=status.HTTP_403_FORBIDDEN)
                
        group = get_object_or_404(UserGroup, id=request.data.get('id'))
        serializer = self.serializer_class(group, data=request.data, partial=True)
        

        if serializer.is_valid():
            serializer.save()

            serialized_group = self.serializer_class(group).data
            return Response({'group': serialized_group, 'message': 'Group updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to update group'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
class DeleteGroupView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        group = UserGroup.objects.filter(id=request.data.get('id'))
        if not request.user.is_staff:
            return Response({'error': 'This service only for admin users'}, status=status.HTTP_403_FORBIDDEN)
        if not group:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            group.delete()
            return Response({'message': 'Group deleted successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to delete group'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class AddUserToGroupView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'This service only for admin users'}, status=status.HTTP_403_FORBIDDEN)
        
        users = request.data.get('users')
        group_id = request.data.get('group')
        
        
        try:
            group = UserGroup.objects.get(id=group_id)
            group.users.add(*users)
            return Response({"message": "Users added successfully"}, status=status.HTTP_200_OK)
        except UserGroup.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({"error": f"IntegrityError: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class RemoveUserFromGroupView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    