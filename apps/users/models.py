from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import CustomUserManager
import secrets


class UserGroup(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    reset_code = models.CharField(max_length=100, blank=True, null=True)
    user_groups = models.ManyToManyField(UserGroup, blank=True, null=True, related_name="user_groups")
    
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.email}'


class TemporaryUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    token = models.CharField(max_length=100, unique=True, default=secrets.token_urlsafe)

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.email} (temporary)'
