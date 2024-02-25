from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import UserGroup
from .serializers import GroupSerializer


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
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class DeleteGroupView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class AddUserToGroupView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class RemoveUserFromGroupView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    