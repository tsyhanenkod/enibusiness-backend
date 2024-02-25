from django.db import models

class UserGroup(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title