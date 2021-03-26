import logging
from django.core.management.base import BaseCommand, CommandError
from pen.models import Tag

class Command(BaseCommand):
    # args = '<target_id target_id ...>'
    help = u'タグをリストアップ'

    def handle(self, *args, **options):
        tags = Tag.objects.all()
        for tag in tags:
            print(tag.name)