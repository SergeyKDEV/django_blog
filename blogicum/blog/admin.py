from django.contrib import admin
from .models import Category, Location, Post, User


empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
