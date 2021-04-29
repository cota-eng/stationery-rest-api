from django.core.management.base import BaseCommand
from pen.models import Product
from time import sleep
import requests
import environ
# import logging
env = environ.Env()
env.read_env('SLACK_WEBHOOK_NEWS')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.related_products.clear()
            sleep(0.1)
        WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_NEWS")
        requests.post(WEB_HOOK_URL, data={
                      'text': "fin! reset related products"})
