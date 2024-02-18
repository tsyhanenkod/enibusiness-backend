from django.urls import path
from .views import *

urlpatterns = [
    path('get_users/', GetUsersView.as_view(), name='get_users'),
    path('get_user/<int:id>', GetUserView.as_view(), name='get_user'),
    path('edit/', EditUserView.as_view(), name='edit_user'),
    path('upload_image/', UploadUserImageView.as_view(), name='upload_image'),
    path('remove_image/', RemoveUserImageView.as_view(), name='remove_image'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
]