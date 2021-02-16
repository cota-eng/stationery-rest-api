from django.contrib import admin
from . import models

admin.site.site_header = "管理画面"

class PenAdmin(admin.ModelAdmin):
    # exclude = ('name',)
    # fields = ('name',)
    list_display = ('name', 'price_yen',)
    list_filter = ('price_yen',)
    # change_list_templates = 'admin/pen/pen_change_list.html'

admin.site.register(models.Pen,PenAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    # list_filter = ('name',)
admin.site.register(models.Tag,TagAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'official_site_link',)
admin.site.register(models.Brand,BrandAdmin)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
admin.site.register(models.Category,CategoryAdmin)


admin.site.register(models.FavPen)
admin.site.register(models.Review)