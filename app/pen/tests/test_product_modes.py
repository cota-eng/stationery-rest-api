from django.test import TestCase
from pen.models import (
    Product,
    Category,
    Tag,
    Brand,
)

"""
各メソッド内で使うユーザー作成、カテゴリ、タグ作成

"""

class ProductModelTests(TestCase):
    
    def setUp(self):

        self.category = Category.objects.create(
            name="鉛筆",
            slug="pencil",
        )

        self.brand = Brand.objects.create(
            name="アイウ工業",
            slug="aiu-factory",
            official_site_link="aiu.example.com"
        )

        self.tag = Tag.objects.create(
            name="安価",
            slug="low-price", 
        )

    def test_create_product_success(self):
        product1 = Product.objects.create(
            name="あいう鉛筆",
            description="",
            price=150,
            image="products/default.jpg",
            image_src="https://example.com",
            amazon_link_to_buy="",
            rakuten_link_to_buy="",
            category=self.category,
            brand=self.brand,
        )
        product1.tag.set([self.tag])
        self.assertTrue(Product.objects.all().exists())