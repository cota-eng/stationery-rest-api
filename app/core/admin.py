from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authentication import models

from django.utils.translation import gettext as _

admin.site.site_title = '管理サイト' 
admin.site.site_header = '文房具レビュー＆閲覧API' 
admin.site.index_title = 'メニュー'

class ProfileInline(admin.TabularInline):
    model = models.Profile
# class AvatarInline(admin.TabularInline):
#     model = models.Avatar

class UserAdmin(BaseUserAdmin):
    inlines = [
        ProfileInline,
        # AvatarInline
    ]
    ordering = ['id',]
    list_display = ['email','username','last_login']
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
        ),
        # (_('avatar'),
        #     {
        #         'fields': ('avatar',)
        #         }
        # ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('email','password1','password2','username')
        }),
    )

admin.site.register(models.User,UserAdmin)
