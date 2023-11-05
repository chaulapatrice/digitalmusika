from django.contrib import admin
from .models import User
# Register your models here.


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'type',
        'province',
        'city'
    )

    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['province', 'city', 'type']
