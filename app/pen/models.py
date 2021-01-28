from django.db import models
import uuid


class Category(models.Model):
    """Model that define category and id is normal"""
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name