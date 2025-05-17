from django.db import models
from django.contrib.auth.models import User as AuthUser

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    user_id = models.CharField(max_length=50, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.email} {self.user_id} ({self.auth_user.username}) - {self.city}"

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name