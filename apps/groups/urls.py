from django.urls import path
from .views import *

urlpatterns = [
    path('get_groups/', GetAllGroupsView.as_view(), name='get_groups'),
    path('get_group/<pk:id>', GetGroupView.as_view(), name='get_group'),
    path('create/', CreateGroupView.as_view(), name='create_group'),
    path('edit/', EditGroupView.as_view(), name='edit_group'),
    path('delete/', DeleteGroupView.as_view(), name='delete_group'),
    path('add_user/', AddUserToGroupView.as_view(), name='add_user_to_group'),
    path('remove_user/', RemoveUserFromGroupView.as_view(), name='remove_user_from_group'),
]
