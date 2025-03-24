from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    title = models.CharField(max_length=40, null=True, blank=True)
    descriptive = models.TextField()

    def __str__(self):
        return self.user.username
    
class multiple(models.Model):
    post = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='uploads/')
    title = models.CharField(max_length=40, null=True, blank=True)
    date = models.DateField(auto_now_add=True) 


class OTPRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)