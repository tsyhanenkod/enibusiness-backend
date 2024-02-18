from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class GetAllGroupsView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class GetGroupView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class CreateGroupView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    

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
    