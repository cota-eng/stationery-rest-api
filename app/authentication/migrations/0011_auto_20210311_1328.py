# Generated by Django 3.1.1 on 2021-03-11 04:28

import core.models
from django.db import migrations
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_auto_20210311_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=core.models.ULIDField(db_index=True, default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=core.models.ULIDField(db_index=True, default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False, unique=True),
        ),
    ]
