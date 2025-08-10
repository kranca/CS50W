from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "last_name", "first_name")

admin.site.register(User, UserAdmin)
admin.site.register(Email)