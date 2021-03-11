from django.contrib import admin
from . import models

admin.site.site_header = "管理画面"

class ReviewInline(admin.TabularInline):
    model = models.Review

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline
    ]
    list_display = ('name', 'price_yen',)
    list_filter = ('price_yen',)

admin.site.register(models.Product,ProductAdmin)

class FavAdmin(admin.ModelAdmin):
    list_display = ('fav_user', 'product',)
    list_filter = ('is_favorite',)

admin.site.register(models.Fav,FavAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)

admin.site.register(models.Tag,TagAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'official_site_link',)

admin.site.register(models.Brand,BrandAdmin)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    
admin.site.register(models.Category,CategoryAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('avarage_star',)

admin.site.register(models.Review,ReviewAdmin)