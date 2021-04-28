import logging
from django.core.management.base import BaseCommand, CommandError
from pen.models import Product
from django.db.models import Q
from pprint import pprint
from time import sleep
import requests
import environ
env = environ.Env()
env.read_env('SLACK_WEBHOOK_NEWS')

class Command(BaseCommand):
    """
    """

    def handle(self, *args, **options):

        # product = Product.objects.get(id="8ceb9878-f374-4d7d-9412-e62a9b7b51fd")
        # related = Product.objects.filter(Q(brand=product.brand.id) | Q(category=product.category.id)).exclude(id=str(product.id)).order_by("?")[:6]
        # print(len(related))
        for product in Product.objects.all():
            related = Product.objects.filter(Q(brand=product.brand.id) | Q(category=product.category.id)).exclude(id=str(product.id)).order_by("?")[:6]
            # related = Product.objects.filter(Q(brand=product.brand.id) | Q(category=product.category.id)).exclude(id=str(product.id)).order_by("?").distinct()[:6]
            product.related_products.set(related)
            product.save()
            # pprint(len(related))
            # pprint(str(product.pk))
        WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_NEWS")
        requests.post(WEB_HOOK_URL, data = {
            'text': "fin! set related products" })
        