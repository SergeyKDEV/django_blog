from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


# UserAdmin.fieldsets += () #ToDo: Remove or finish Admin fields

admin.site.register(MyUser, UserAdmin)
