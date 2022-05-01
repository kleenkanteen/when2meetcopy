from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event, Available

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Event)
admin.site.register(Available)