# Generated by Django 3.1.1 on 2021-02-16 06:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pen', '0002_remove_review_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favpen',
            name='fav_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_fav', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favpen',
            name='pen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pen_fav', to='pen.pen'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars_of_design',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='design'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars_of_durability',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='durability'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars_of_easy_to_get',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='easy_to_get'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars_of_function',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='function'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars_of_usefulness',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='usefulness'),
        ),
    ]
