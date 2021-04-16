from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import exceptions
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from . import models
from django.utils.text import gettext_lazy as _

# class LoginSerializer(serializers.ModelSerializer):
#     tokens = serializers.SerializerMethodField()
#     email = serializers.EmailField(max_length=255)
#     password = serializers.CharField(max_length=255, min_length=4, write_only=True)
#     tokens = serializers.CharField(read_only=True)
#     class Meta:
#         model = models.User
#         fields = ('email', 'password','tokens',)
#     # need to check
#     def get_tokens(self, obj):
#         user = models.User.objects.get(email=obj['email'])
#         return {
#             'access':user.tokens()['access'],
#             'refresh':user.tokens()['refresh'],
#         }
import environ
env = environ.Env()
env.read_env('.env')
import requests, json
from pen.models import Review,FavProduct


# class AvatarSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    # def get_id(self, obj):
    #     return obj.profile.pk
    # class Meta:
    #     model = models.Avatar
    #     fields = ('id','image',)


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField(read_only=True)
    twitter_account = serializers.ReadOnlyField(source="profile.twitter_account")
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        avatar = obj.profile.avatar
        if avatar:
            return avatar
        return None

    def get_nickname(self, obj):
        return obj.profile.nickname

    class Meta:
        model = get_user_model()
        fields = ('id','profile','nickname','twitter_account','avatar',)
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            # 'email': {
            #     'read_only':True
            # },
        }

    @staticmethod
    def setup_for_query(queryset):
        """
        to many - 
        to one  - profile, avatar
        """
        queryset = queryset.prefetch_related()
        queryset = queryset.select_related('profile',)
        return queryset
    # def create(self, validated_data):
    #     response = super().create(validated_data)
    #     WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_CREATE_USER")
    #     requests.post(WEB_HOOK_URL, data = json.dumps({
    #         'text': f':smile_cat:UserCreated [ {validated_data["email"]} ] ',  
    #     }))
    #     return response
    # def create(self, validated_data):
    #     return get_user_model().objects.create_user(**validated_data)
from pen.serializers import ReviewNotIncludeUserSerialier,FavUsedByProfileSerializer

class WhoAmISerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        avatar = obj.avatar
        if avatar:
            return avatar
        return None
    class Meta:
        model = models.Profile
        fields = ('id','nickname','avatar', 'user')
       

class OwnProfileEditSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # user_profile = UserSerializer()
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        avatar = obj.avatar
        if avatar:
            return avatar.name
        return None
    # avatar = AvatarSerializer()

    class Meta:
        model = models.Profile
        fields = ('id', 'nickname','user', 'avatar','twitter_account')
        read_only_fields = ('user',)
class ProfileSerializer(serializers.ModelSerializer):
    """
    read only 
    """
    # user = UserSerializer(read_only=True)
    created_at = serializers.DateField(format="%Y/%m/%d",read_only=True)
    updated_at = serializers.DateField(format="%Y/%m/%d", read_only=True)
    # user_profile = UserSerializer()
    review = serializers.SerializerMethodField()
    faved_product = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        avatar = obj.avatar
        if avatar:
            return avatar
        return None
    # avatar = AvatarSerializer()

    def get_review(self, obj):
        own_review = Review.objects.filter(reviewer__id=obj.user.id)
        print(own_review)
        serializer = ReviewNotIncludeUserSerialier(instance=own_review,many=True)
        return serializer.data
    
    @staticmethod
    def setup_for_query(queryset):
        # to-one
        qs = queryset.select_related().prefetch_related()
        return qs
    # def get_faved_product(self, obj):
    #     faved_product = FavProduct.objects.filter(fav_user=obj.user)
    #     print(faved_product)
    #     serializer = FavProductSerializer(instance=faved_product, many=True)
    #     return serializer.data


    class Meta:
        model = models.Profile
        fields = ('id','nickname','review','faved_product','created_at', 'updated_at','avatar', )
        # fields = ('id', 'nickname','created_at', 'updated_at',  'avatar', 'user_profile')
        # extra_kwargs = {'user_profile': {'read_only': True}}
    # def validate(self, attrs):
    #     nickname = attrs.get('nickname')
    #     if not nickname.isalnum():
    #         raise serializers.ValidationError('only a-z 0-9 alnum')
    #     return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': _('invalid token')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


# class AvatarSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.Profile
#         fields = ('avatar',)

#     def save(self, *args, **kwargs):
#         prev_avatar = self.instance.avatar
#         if prev_avatar:
#             prev_avatar.delete()
#         return super().save(*args, **kwargs)
    
#     def update(self, instance, validated_data):
#         return super().update(instance, validated_data)

# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(style={'input_type':'password'},write_only=True)
#     password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'password','password2',)
#         extra_kwargs = {'password': {'write_only': True}}

#     def save(self):
#         user = get_user_model().objects.create_user(
#             email=self.validated_data['email']
#         )
#         password = self.validated_data['password']
#         password2 = self.validated_data['password2']
#         if  password != password2:
#             raise serializers.ValidationError(
#                 {'error':'password must be equal'})
#         user.set_password(password)
#         user.save()



# class EmailVerifySerializer(serializers.ModelSerializer):
#     tokens = serializers.CharField(max_length=500)
#     class Meta:
#         model = get_user_model
#         fields = ('tokens',)
        
# class LoginSerializer(serializers.ModelSerializer):
#     tokens = serializers.SerializerMethodField()
#     email = serializers.EmailField(max_length=255)
#     password = serializers.CharField(max_length=255, min_length=4, write_only=True)
#     tokens = serializers.CharField(read_only=True)
#     class Meta:
#         model = get_user_model
#         fields = ('email', 'password','tokens',)
#     # need to check
#     def get_tokens(self, obj):
#         user = models.User.objects.get(email=obj['email'])
#         return {
#             'access':user.tokens()['access'],
#             'refresh':user.tokens()['refresh'],
#         }

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         filtered_user_by_email = models.User.objects.filter(email=email)
#         user = authenticate(email=email, password=password)
#         if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
#             raise exceptions.AuthenticationFailed(
#                 detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

#         if not user:
#             raise exceptions.AuthenticationFailed('invalid user')
#         if not user.is_active:
#             raise exceptions.AuthenticationFailed('contact administrator')
#         if not user.is_verified:
#             raise exceptions.AuthenticationFailed('email is not verified')
#         return {
#             'email': user.email,
#             'tokens':user.tokens,
#         }



# class PasswordResetSerializer(serializers.ModelSerializer):
#     redirect_url = serializers.CharField(max_length=255, required=False)
    
#     class Meta:
#         model = models.User
#         fields = ('email','redirect_url',)

    # def validate(self, attrs):
    #     email = attrs['data'].get('email')
    #     user = models.User.objects.filter(email=email)
    #     if user.exists():
    #         uidb64 = urlsafe_base64_encode(user.id)
    #         token = PasswordResetTokenGenerator().make_token(user)
    #         current_site = get_current_site(request=attrs['data'].get('request')).domain
    #         reverse_link = reverse('account:password-reset',kwargs={'uidb64':uidb64,'token':token})
    #         absolute_url = f'http://{current_site}{reverse_link}'

    #         email_body = f'Hi,there! \n please click this url for reset your password! \n {absolute_url}'

    #         data = {
    #             'email_subject': 'reset password',
    #             'email_body': email_body,
    #             'email_to': user.email,
    #             }
            
    #         utils.Util.send_email(data)
    #     return super().validate(attrs)
    
# class SetNewPasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     token = serializers.CharField(write_only=True)
#     uidb64 = serializers.CharField(write_only=True)
#     class Meta:
#         model = models.User
#         fields = ('password', 'token', 'uidb64',)
    
#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             token = attrs.get('token')
#             uidb64 = attrs.get('uidb64')
#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = models.User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise exceptions.AuthenticationFailed('reset link is invalid, try again!', 401)
#             user.set_password(password)
#             user.save()
#         except  Exception as e:
#                 raise exceptions.AuthenticationFailed('reset link is invalid, try again!', 401)
                
#         return super().validate(attrs)