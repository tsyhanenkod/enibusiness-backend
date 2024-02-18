from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class GetUsersView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class GetUserView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class EditUserView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class UploadUserImageView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class RemoveUserImageView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
    
class DeleteUserView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
    
