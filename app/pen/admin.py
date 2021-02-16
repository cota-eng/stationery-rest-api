from django.contrib import admin
from . import models

admin.site.register(models.Tag)
admin.site.register(models.Brand)
admin.site.register(models.Pen)
admin.site.register(models.Category)
admin.site.register(models.FavPen)
admin.site.register(models.Review)