# Generated by Django 3.1.1 on 2021-04-06 01:32

import core.models
from django.db import migrations
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('pen', '0025_auto_20210406_0811'),
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
