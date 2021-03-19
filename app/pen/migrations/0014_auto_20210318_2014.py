# Generated by Django 3.1.1 on 2021-03-18 11:14

import core.models
from django.db import migrations
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('pen', '0013_auto_20210318_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=core.models.ULIDField(db_index=True, default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='id',
            field=core.models.ULIDField(db_index=True, default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False, unique=True),
        ),
    ]