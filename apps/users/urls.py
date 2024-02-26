from django.urls import path
from .views import *


urlpatterns = [
    path('get_users/', GetUsersView.as_view(), name='get_users'),
    path('edit/', EditUserView.as_view(), name='edit_user'),
    path('edit_business/', EditBusinessDataView.as_view(), name='edit_business'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile_image/', ProfileImageView.as_view(), name='profile_image'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
]

