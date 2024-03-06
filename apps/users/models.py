from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import CustomUserManager
import secrets

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    social_media = models.CharField(max_length=100, blank=True, null=True)
    reset_code = models.CharField(max_length=100, blank=True, null=True)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.email}'


class TemporaryUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    group = models.CharField(max_length=5, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    token = models.CharField(max_length=100, unique=True, default=secrets.token_urlsafe)

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.email} (temporary)'
    

class Referal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    refered_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='refered_user')
    project = models.CharField(max_length=250, blank=True, null=True)
    amount = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} refered {self.refered_user}'
