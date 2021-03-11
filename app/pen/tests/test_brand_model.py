from django.test import TestCase
from rest_framework.test import APIClient
from ..models.brand import Brand
from django.urls import reverse
from rest_framework import status
from .. import serializers
"""
作成するTestCase
モデルの作成success,fail(error)
failは、空欄、
モデルUpdate
CRUD対応のものはCRUD

"""
BRAND_LIST_URL = reverse('pen:brand-list')

class BrandAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_brand_success(self):
        Brand.objects.create(
            name="brand1",
            slug="brand1",
            official_site_link="brand1"
        )
        res = self.client.get(BRAND_LIST_URL)
        tags = Brand.objects.all()
        serializer = serializers.BrandSerializer
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_brand_fail(self):
        payload = {
            'name': '',
            'slug': '',
            'official_site_link':"tag1.com"
            }
        res = self.client.post(BRAND_LIST_URL)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)