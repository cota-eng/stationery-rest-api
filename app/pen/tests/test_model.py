from django.test import TestCase
from .. import models

class ModelTests(TestCase):
    def test_create_valid_category(self):
        _name = "シャーペン"
        category = models.Category.objects.create(
            name=_name
        )
        self.assertEqual(category.name,_name)
    