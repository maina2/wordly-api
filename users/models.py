from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    bio=models.TextField(max_length=100,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    website=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.username
    