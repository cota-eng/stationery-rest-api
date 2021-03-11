from django.db import models
import uuid
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils import timezone
from authentication.models import User
import ulid
from core.models import ULIDField


class Brand(models.Model):
    """
    Model that define Maker and has name and only one official web site
    """
    name = models.CharField(
        _('brand name'),
        max_length=50,
        unique=True,
    )
    slug = models.CharField(
        _("brand slug"),
        max_length=50,
        unique=True,
        )
    official_site_link = models.CharField(
         _("brand link"),
         max_length=255,
         unique=True
         )

    def __str__(self):
        return f'Productor: {self.name}'
