from django.contrib import admin

from bot.models import User, Skill, City, Section

# Register your models here.
admin.site.register(Skill)
admin.site.register(User)
admin.site.register(City)
admin.site.register(Section)