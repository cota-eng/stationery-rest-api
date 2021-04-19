from django.shortcuts import render
from rest_framework import views
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from . import serializers
from django.conf import settings
from rest_framework import exceptions
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from rest_framework.permissions import (AllowAny,IsAuthenticated,)
from rest_framework import  status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import LogoutSerializer
from .permissions import UserIsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import parsers
from rest_framework import mixins
from rest_framework import generics
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.shortcuts import redirect
# from django.http import HttpResponsePermanentRedirect

"""
4 views needed
- Google login 
- user profile list/get read only
- profile update only owner
- logout
"""

class GoogleLogin(SocialLoginView):
    """
    For google oauth
    """
    authentication_classes = [] 
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client


class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    TODO:not needed?
    変更可能な情報はprofileにのみ存在してるから、、、
    UserRankingなどに必要かも
    """
    # TODO: serializer - 
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = "id"

    def get_queryset(self):
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        return qs

class WhoAmIView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    # TODO: serializer - ok
    queryset = models.Profile.objects.all()
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.WhoAmISerializer
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ProfileReadOnlyViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    queryset = models.Profile.objects.all().prefetch_related("user__reviewer")
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (AllowAny,)
    serializer_class = serializers.ProfileSerializer
    #TODO serializer Recreate
    # parser_classes = [parsers.MultiPartParser,
    #                   parsers.FormParser,]
    def get_queryset(self):
        qs = self.queryset
        qs = self.get_serializer_class().setup_for_query(qs)
        return qs

class OwnProfileListRetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                                          mixins.ListModelMixin,
                                          mixins.UpdateModelMixin,
                                          viewsets.GenericViewSet):
    """
    for your own profile
    """
    queryset = models.Profile.objects.all()
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (IsAuthenticated,
                          UserIsOwnerOrReadOnly,
                          )
    serializer_class = serializers.OwnProfileEditSerializer
    """for img uplaod"""
    # parser_classes = [parsers.MultiPartParser,
    #                   parsers.FormParser,]
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class LoginAPIView(generics.GenericAPIView):
#     authentication_classes = [] # disable authentication
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = serializers.LoginSerializer
#     def post(self, request):
#         serialier = self.serializer_class(data=request.data)
#         serialier.is_valid(raise_exception=True)

#         return Response(serialier.data,status=status.HTTP_200_OK)

# class AvatarRetrieveUpdateView( mixins.RetrieveModelMixin,
#                         mixins.ListModelMixin,
#                         mixins.UpdateModelMixin,
#                         viewsets.GenericViewSet):
#     """
#     if not own profile
#     404 when access to your own image & cannot change image
#     """
#     queryset = models.Profile.objects.all()
#     parser_classes = (parsers.MultiPartParser,
#                       parsers.FormParser,)
#     permission_classes = (
#         permissions.IsAuthenticated,
#         # UserIsOwnerOrReadOnly,
#     )
#     serializer_class = serializers.AvatarSerializer
    
    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)
    # def destroy(self, request, *args, **kwargs):
    #     """
    #     delete is invalid
    #     """
    #     response = {'message': 'DELETE method is not allowed'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     """
    #     list is invalid
    #     """
    #     response = {'message': 'list method is not allowed'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, *args, **kwargs):
    #     """
    #     psot is invalid
    #     """
    #     response = {'message': 'post method is not allowed'}
    #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
   
