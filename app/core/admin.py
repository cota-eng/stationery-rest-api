from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account import models

from django.utils.translation import gettext as _

class UserAdmin(BaseUserAdmin):
    ordering = ['id',]
    list_display = ['email',]
    fieldsets = (
        (_('Credentials'),{'fields':('email','password')}),
        (_('Personal Info'),{'fields':('is_verified',)}),
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
