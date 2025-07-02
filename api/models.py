from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ops', 'Ops User'),
        ('client', 'Client User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    is_verified = models.BooleanField(default=False)

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
