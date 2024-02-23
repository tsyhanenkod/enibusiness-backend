from django.urls import path
from .views import *


urlpatterns = [
    path('get_users/', GetUsersView.as_view(), name='get_users'),
    path('edit/', EditUserView.as_view(), name='edit_user'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
]

