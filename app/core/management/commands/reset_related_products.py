import logging
from django.core.management.base import BaseCommand, CommandError
from pen.models import Product
from django.db.models import Q
from pprint import pprint
from time import sleep
class Command(BaseCommand):
    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.related_products.clear()
            sleep(0.1)