import logging
from django.core.management.base import BaseCommand, CommandError
from pen.models import Product
from django.db.models import Q
from pprint import pprint
from time import sleep
class Command(BaseCommand):
    """
    """

    def handle(self, *args, **options):
        for product in Product.objects.all():
            related = Product.objects.filter(Q(brand=product.brand.id) | Q(category=product.category.id)).exclude(id=str(product.id)).order_by("?").distinct()[:6]
            product.related_products.set(related)
            # pprint(related)
            # pprint(str(product.pk))
            sleep(0.1)