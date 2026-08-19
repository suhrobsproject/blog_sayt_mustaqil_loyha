from django.db import models
from django.contrib.auth.models import AbstractUser
from baseapp.models import BaseModel

class CustomUser(AbstractUser, BaseModel):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    social = models.URLField(null=True, blank=True)
    websites = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username