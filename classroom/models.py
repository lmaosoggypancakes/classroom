from django.db import models
from django.contrib.auth.models import AbstractUser
import time, django.utils.timezone as timezone
# Create your models here.

class User(AbstractUser):
    pass
    is_teacher = models.BooleanField()
    homework = models.ManyToManyField("Assignment", related_name="assignments", symmetrical=False)
    def serialize(self):
        return {
            "username": self.username,
            "id": self.id,
            "is_teacher": self.is_teacher,
            "timestamp": self.last_login.strftime("%b %#d %Y, %#I:%M %p"),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
    def __str__(self):
        return self.username
class Classroom(models.Model):
    name = models.CharField(max_length=64, default="null")
    student = models.ManyToManyField("User", related_name="classroom", symmetrical=False, blank=True)
    teacher = models.ForeignKey("User", related_name="teachers", on_delete=models.CASCADE)
    join_code = models.IntegerField()
    picture = models.URLField()
    def serialize(self):
        pass
class Assignment(models.Model):
    question = models.CharField(max_length=64)
    body = models.CharField(max_length=200)
    due_date = models.DateTimeField(auto_now_add=False)
    assigned_to = models.ForeignKey("User", related_name="assignments", on_delete=models.CASCADE, default=None)
    date_turned_in = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    in_class = models.ForeignKey("Classroom", related_name="class_assignments", on_delete=models.CASCADE)
    late =  models.BooleanField(default=False)
    def serialize(self):
        pass

class PasswordReset(models.Model):
    hashed_code = models.TextField()
    for_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    time = models.DateTimeField(auto_now_add=True)

    