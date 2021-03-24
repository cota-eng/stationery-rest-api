from django.test import TestCase
from rest_framework.test import APIClient
from pen.models import Brand
from django.urls import reverse
from rest_framework import status
from pen.serializers import BrandSerializer
"""
作成するTestCase
モデルの作成success,fail(error)
fail　空欄、字数制限、だぶり
brand list,retrieve only
"""
BRAND_LIST_URL = reverse('pen:brand-list')

class BrandTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_brand_success(self):
        SampleBrand = Brand.objects.create(
            id=1,
            name="brand1",
            slug="brand1",
            official_site_link="brand1.com"
        )
        res = self.client.get(BRAND_LIST_URL)
        brands = Brand.objects.all()
        self.assertEqual(brands.count(),1)
        self.assertEqual(len(res.data),1)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["name"], SampleBrand.name)
    
    def test_create_brand_fail_by_invalid_method(self):
        payload = {
            'name': 'brand2',
            'slug': 'brand2',
            'official_site_link':"brand2.com"
            }
        res = self.client.post(BRAND_LIST_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_brand_fail_by_not_unique(self):
        brand1 = Brand.objects.create(
            id=1,
            name="brand1",
            slug="brand1",
            official_site_link="brand1.com"
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Brand.objects.create(
            id=2,
            name="brand1",
            slug="brand1",
            official_site_link="brand1.com"
            )

    def test_create_brand_fail_by_blank(self):
        Brand.objects.create(
            id=1,
            name="",
            slug="brand",
            official_site_link="brand.com"
        )
        self.assertEqual(Brand.objects.filter(name="").count(),1)
        
