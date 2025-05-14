from django.db import models
from django.contrib.auth.models import User as AuthUser

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill, blank=True)
    cities = models.ManyToManyField('City', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.auth_user.username}) - {self.email}"

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name