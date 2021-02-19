from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authentication import models

from django.utils.translation import gettext as _

class ProfileInline(admin.TabularInline):
    model = models.Profile

class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline
    ]
    ordering = ['id',]
    list_display = ['email',]
    fieldsets = (
        (_('Credentials'),{'fields':('email','password','username')}),
        # (_('Personal Info'),{'fields':('is_verified',)}),
        (_('Permissions'),
            {
                'fields': ('is_active',
                           'is_staff',
                           'is_superuser')
            }
        ),
        (_('Important dates'),
            {
                'fields': ('last_login',)
                }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('email','password1','password2')
        }),
    )

admin.site.register(models.User,UserAdmin)
