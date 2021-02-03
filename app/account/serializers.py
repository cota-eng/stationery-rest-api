from rest_framework import serializers
from django.conf import settings
from . import models
from django.contrib.auth import get_user_model,authenticate
from rest_framework import exceptions
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
        nickname = attrs.get('nickname', '')
        if not nickname.isalnum():
            raise serializers.ValidationError('only a-z 0-9 alnum')


class EmailVerifySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=500)
    class Meta:
        model = models.User
        fields = ('token',)
        
class LoginSerializer(serializers.ModelSerializer):
    tokens = serializers.CharField(max_length=500, read_only=True)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=4, write_only=True)
    tokens = serializers.CharField(read_only=True)
    class Meta:
        model = models.User
        fields = ('email', 'password','tokens',)
        
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password', '')
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