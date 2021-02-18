from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid
import os
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _



class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user( email, password, **extra_fields)

AUTH_PROVIDERS = {
    'google': 'google',
    'email':'email',
}

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    and using uuid4
    """
    id = models.UUIDField(
        _('uuid'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True)
    email = models.EmailField(_('email'),max_length=255, unique=True)
    is_verified = models.BooleanField(_('verified'),default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    auth_provider = models.CharField(
        max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email')
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        }

def profile_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/avatar/',filename)

def profile_avatar_resize():
    pass

class Profile(models.Model):
    """Model that has avatar and dates of create and update"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user_profile = models.OneToOneField(
        # _('user'),
        User,
        related_name="user_profile",
        on_delete=models.CASCADE
        )
    nickname = models.CharField(_('nickname'),max_length=50,default="匿名ユーザー")
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
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