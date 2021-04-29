from django.core.management.base import BaseCommand
from pen.models import Tag
# import logging


class Command(BaseCommand):
    help = u'タグをリストアップ'

    def handle(self, *args, **options):
        tags = Tag.objects.all()
        for tag in tags:
            print(tag.name)
