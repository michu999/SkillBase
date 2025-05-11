from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, null=False, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(post_save, sender=AuthUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(
            auth_user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name or instance.username)