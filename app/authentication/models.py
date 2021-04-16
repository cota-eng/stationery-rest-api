from django.db import models
import uuid
import os
import environ
import requests
import json
import ulid
from django.contrib.auth.models import (AbstractBaseUser, 
                                       BaseUserManager,
                                       PermissionsMixin)
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import ULIDField

env = environ.Env()
env.read_env('.env')

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    """
    TODO: id override to UUOD ?
    """
    id = ULIDField(
        primary_key=True,
        default=ulid.new,
        unique=True,
        editable=False,
        db_index=True
        )
    # oauth email automatically add
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'),unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True


def profile_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    # return os.path.join('uploads/avatar/',filename)
    return os.path.join('avatar/',filename)


# class Avatar(models.Model):
#     name = models.CharField(_("name"),max_length=20,null=True,blank=True)
#     image = models.ImageField(upload_to="avatar",  width_field=None, height_field=None, null=True, blank=True)
#     def __str__(self):
#         return f'{self.image}'
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid
class Profile(models.Model):
    """
    Model that has avatar and dates of create and update
    TODO: id is to normal id?
    """
    # uuid = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     unique=True,
    #     db_index=True,
    #     editable=False)
    id = ULIDField(
        primary_key=True,
        default=ulid.new,
        unique=True,
        editable=False,
        db_index=True
        )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE
        )
    nickname = models.CharField(_('nickname'),max_length=10,default="匿名ユーザー")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    avatar = ProcessedImageField(
        upload_to=profile_avatar_path,
        processors=[ResizeToFill(500,500)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True,
        default="avatar/default.jpg"
        )
    # avatar = models.ForeignKey(Avatar,on_delete=models.PROTECT,related_name="profile")
    twitter_account = models.CharField(_('twitter username'),null=True,blank=True,max_length=100)
    def __str__(self):
        return f'Profile of {self.user}'

from django.db.models.signals import post_save

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """
    when user created, own profile automatically created
    """
    if kwargs['created']:
        # WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_CREATE_USER")
        # requests.post(WEB_HOOK_URL, data = json.dumps({
        #     'text': f':smile_cat:Profile [ {kwargs["instance"]} ] Created!!',  
        # }))
        # avatar = Avatar.objects.get(pk=1)
        profile = Profile.objects.get_or_create(user=kwargs['instance'])