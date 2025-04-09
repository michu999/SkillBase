from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"