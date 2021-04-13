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
            related = Product.objects.exclude(pk=product.pk).filter(Q(related_products__brand__pk=product.brand.id)| Q(related_products__category__pk=product.category.id)).order_by("?").distinct()[:6]
            # related = Product.objects.all().order_by("?")[:6]
            # Q(related_products__tag__pk=product.tag.pk)
            # Product.objects.create(product=product,related_products=related)
            product.related_products.set(related)
            # pprint(product.related_products.all())
            pprint(product)
            # pprint(related)
            sleep(0.5)