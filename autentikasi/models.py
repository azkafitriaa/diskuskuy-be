from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    ROLE_CHOICES = [
        ('student', 'student'),
        ('lecturer', 'lecturer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    name = models.CharField(max_length=100)
    photo_url = models.TextField(default=None, blank=True, null=True)
    # photo = models.ImageField(upload_to="profile_photo", default=None, blank=True, null=True)

    REQUIRED_FIELDS = ('user','role')

    def __str__(self):
        return self.user.username

class Student(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    npm = models.CharField(max_length=10)

class Lecturer(models.Model):
    lecturer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nim = models.CharField(max_length=10)
