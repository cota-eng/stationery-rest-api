from rest_framework import serializers
from django.conf import settings
from . import models
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework import exceptions
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from . import utils
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format="%Y-%m-%d",read_only=True)
    updated_at = serializers.DateField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = models.Profile
        fields = ('id', 'nickname', 'created_at', 'updated_at', 'avatar', 'user_profile')
        extra_kwargs = {'user_profile': {'read_only': True}}

    def validate(self, attrs):
        nickname = attrs.get('nickname')
        if not nickname.isalnum():
            raise serializers.ValidationError('only a-z 0-9 alnum')


class EmailVerifySerializer(serializers.ModelSerializer):
    tokens = serializers.CharField(max_length=500)
    class Meta:
        model = models.User
        fields = ('tokens',)
        
class LoginSerializer(serializers.ModelSerializer):
    tokens = serializers.CharField(max_length=500, read_only=True)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=4, write_only=True)
    tokens = serializers.CharField(read_only=True)
    class Meta:
        model = models.User
        fields = ('email', 'password','tokens',)
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise exceptions.AuthenticationFailed('invalid user')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('contact administrator')
        if not user.is_verified:
            raise exceptions.AuthenticationFailed('email is not verified')
        return {
            'email': user.email,
            'tokens':user.tokens,
        }

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email',)

    def validate(self, attrs):
        email = attrs['data'].get('email')
        user = models.User.objects.filter(email=email)
        if user.exists():
            uidb64 = urlsafe_base64_encode(user.id)
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=attrs['data'].get('request')).domain
            reverse_link = reverse('account:password-reset-check',kwargs={'uidb64':uidb64,'token':token})
            absolute_url = f'http://{current_site}{reverse_link}'

            email_body = f'Hi,there! \n please click this url for reset your password! \n {absolute_url}'

            data = {
                'email_subject': 'reset password',
                'email_body': email_body,
                'email_to': user.email,
                }
            
            utils.Util.send_email(data)
        return super().validate(attrs)            