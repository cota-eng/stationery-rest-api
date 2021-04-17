import logging
from django.core.management.base import BaseCommand, CommandError
from pen.models import Product
from django.db.models import Q
from pprint import pprint
from time import sleep
import requests

env = environ.Env()
env.read_env('SLACK_WEBHOOK_NEWS')

class Command(BaseCommand):
    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.related_products.clear()
            sleep(0.1)
        WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_NEWS")
        requests.post(WEB_HOOK_URL, data = {
            'text': "fin! set related products" })