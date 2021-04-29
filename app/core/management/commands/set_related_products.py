# import logging
from django.core.management.base import BaseCommand
from pen.models import Product
from django.db.models import Q
# from time import sleep
import requests
import environ
env = environ.Env()
env.read_env('SLACK_WEBHOOK_NEWS')


class Command(BaseCommand):

    def handle(self, *args, **options):
        for product in Product.objects.all():
            related = Product.objects.filter(Q(brand=product.brand.id) | Q(
                category=product.category.id)) \
                    .exclude(id=str(product.id)) \
                    .order_by("?")[:6]
            product.related_products.set(related)
            product.save()
        WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_NEWS")
        requests.post(WEB_HOOK_URL, data={
            'text': "fin! set related products"})
