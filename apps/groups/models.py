from django.db import models
from apps.users.models import CustomUser


class UserGroup(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=250, null=True, blank=True)
    users = models.ManyToManyField(CustomUser, related_name='user_groups', blank=True)

    def __str__(self):
        return self.title