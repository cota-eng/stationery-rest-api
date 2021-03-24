from django.test import TestCase
from rest_framework.test import APIClient
from pen.models import Category
from django.urls import reverse
from rest_framework import status

CATEGORY_LIST_URL = reverse('pen:category-list')

class CategoryTests(TestCase):
    name = "category1"
    slug = "category1"
    # def setUp(self):
    #     self.client = APIClient()

    def test_create_category_success(self):
        SampleCategory = Category.objects.create(
            id=1,
            name=self.name,
            slug=self.slug
        )
        res = self.client.get(CATEGORY_LIST_URL)
        category = Category.objects.all()
        self.assertEqual(category.count(),1)
        self.assertEqual(len(res.data),1)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["name"], SampleCategory.name)
    
    def test_create_category_fail_by_invalid_method(self):
        payload = {
            'name': self.name,
            'slug': self.slug,
            }
        res = self.client.post(CATEGORY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_category_fail_by_not_unique(self):
        category1 = Category.objects.create(
            id=1,
            name=self.name,
            slug=self.slug,
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(
            id=2,
            name=self.name,
            slug=self.slug,
            )

    def test_create_category_fail_by_blank(self):
        Category.objects.create(
            id=1,
            name="",
            slug=self.slug,
        )
        self.assertEqual(Category.objects.filter(name="").count(),1)
        
