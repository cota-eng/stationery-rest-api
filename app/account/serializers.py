from rest_framework import serializers
from django.conf import settings
from . import models
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id','email', 'password',)
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
