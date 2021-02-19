from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, 
                                       BaseUserManager,
                                       PermissionsMixin)
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid
import os
from rest_framework_simplejwt.tokens import RefreshToken
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.conf import settings


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

    # def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
    #     if backend is None:
    #         backends = auth._get_backends(return_tuples=True)
    #         if len(backends) == 1:
    #             backend, _ = backends[0]
    #         else:
    #             raise ValueError(
    #                 'You have multiple authentication backends configured and '
    #                 'therefore must provide the `backend` argument.'
    #             )
    #     elif not isinstance(backend, str):
    #         raise TypeError(
    #             'backend must be a dotted import path string (got %r).'
    #             % backend
    #         )
    #     else:
    #         backend = auth.load_backend(backend)
    #     if hasattr(backend, 'with_perm'):
    #         return backend.with_perm(
    #             perm,
    #             is_active=is_active,
    #             include_superusers=include_superusers,
    #             obj=obj,
    #         )
    #     return self.none()


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
    # nickname = models.CharField(
    #     _('nickname'),
    #     max_length=150,
    #     default='初期ユーザー'
    # )
    # first_name = models.CharField(_('first name'), max_length=150, blank=True)
    # last_name = models.CharField(_('last name'), max_length=150, blank=True)
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

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # def get_full_name(self):
    #     """
    #     Return the first_name plus the last_name, with a space in between.
    #     """
    #     full_name = '%s %s' % (self.first_name, self.last_name)
    #     return full_name.strip()

    # def get_short_name(self):
    #     """Return the short name for the user."""
    #     return self.first_name


def profile_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    # return os.path.join('uploads/avatar/',filename)
    return os.path.join('media/',filename)

def profile_avatar_resize():
    pass

class Profile(models.Model):
    """Model that has avatar and dates of create and update"""
    """
    TODO: id is to normal id?
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user_profile = models.OneToOneField(
        # _('user'),
        settings.AUTH_USER_MODEL,
        related_name="user_profile",
        on_delete=models.CASCADE
        )
    nickname = models.CharField(_('nickname'),max_length=50,default="匿名ユーザー")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    avatar = models.ImageField(upload_to=profile_avatar_path, height_field=None, width_field=None, max_length=None,null=True,blank=True)
    twitter_account = models.CharField(_('twitter username'),null=True,blank=True,max_length=100)
    # favorite_pen = models.ManyToManyField()
    def __str__(self):
        return f'Profile of {self.nickname}'

from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """ 新ユーザー作成時に空のprofileも作成する """
    if kwargs['created']:
        user_profile = Profile.objects.get_or_create(user_profile=kwargs['instance'])