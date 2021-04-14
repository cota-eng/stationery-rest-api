from django.contrib import admin
from .models import Profile, User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','created_at',)
    # list_filter = ('name',)


# class AvatarAdmin(admin.ModelAdmin):
    # list_display = ('name','image')

admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Avatar,AvatarAdmin)