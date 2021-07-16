from django.contrib import admin
from .models import User, Address
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Address)

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('phone', 'username', 'first_name')
    # The fields by which the entries should be searchable
    list_filter = ('is_active', 'is_staff')
    # The Options that should be available for filtering
    ordering = ('first_name',)
    # The order in which the entries are displayed
    list_display = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff')
    # Columns to display at the all users page
    fieldsets = ((None, {'fields': ('phone', 'first_name', 'last_name')}),
    ('Permissions', {'fields': ('is_staff', 'is_active')}))
    # The fields to display at user update area
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'password1', 'password2', 'address', 'gstin')
        }),
    )

admin.site.register(User, UserAdminConfig)