from django.urls import path
from .views import *

urlpatterns = [
    path('get_groups/', GetAllGroupsView.as_view(), name='get_groups'),
    path('get_my_eni_grops_users/', GetMyEniGroupsUsers.as_view(), name='get_my_eni_grops_users'),
    path('get_group/<int:id>', GetGroupView.as_view(), name='get_group'),
    path('create_group/', CreateGroupView.as_view(), name='create_group'),
    path('edit/', EditGroupView.as_view(), name='edit_group'),
    path('delete/', DeleteGroupView.as_view(), name='delete_group'),
    path('add_users/', AddUserToGroupView.as_view(), name='add_user_to_group'),
    path('remove_users/', RemoveUserFromGroupView.as_view(), name='remove_user_from_group'),
]
