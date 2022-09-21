from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', "first_name", "last_name", 'phone', 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    search_fields = ('email',)
    ordering = ('-created',)


admin.site.register(User, CustomUserAdmin)
