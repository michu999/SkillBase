from django.contrib import admin

from bot.models import User, Skill, City

# Register your models here.
admin.site.register(Skill)
admin.site.register(User)
admin.site.register(City)