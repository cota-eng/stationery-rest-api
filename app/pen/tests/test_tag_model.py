from django.test import TestCase
from rest_framework.test import APIClient
from pen.models import Tag
from django.urls import reverse
from rest_framework import status
from pen.serializers import BrandSerializer
TAG_LIST_URL = reverse('pen:tag-list')

class TagTests(TestCase):
    name = "tag1"
    slug = "tag1"
    # def setUp(self):
    #     self.client = APIClient()

    def test_create_tag_success(self):
        SampleTag = Tag.objects.create(
            id=1,
            name=self.name,
            slug=self.slug
        )
        res = self.client.get(TAG_LIST_URL)
        tag = Tag.objects.all()
        self.assertEqual(tag.count(),1)
        self.assertEqual(len(res.data),1)
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["name"], SampleTag.name)
    
    def test_create_tag_fail_by_invalid_method(self):
        payload = {
            'name': self.name,
            'slug': self.slug,
            }
        res = self.client.post(TAG_LIST_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_tag_fail_by_not_unique(self):
        tag1 = Tag.objects.create(
            id=1,
            name=self.name,
            slug=self.slug,
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Tag.objects.create(
            id=2,
            name=self.name,
            slug=self.slug,
            )

    def test_create_tag_fail_by_blank(self):
        Tag.objects.create(
            id=1,
            name="",
            slug=self.slug,
        )
        self.assertEqual(Tag.objects.filter(name="").count(),1)
        
