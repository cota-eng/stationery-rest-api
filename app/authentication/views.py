from django.shortcuts import render
from rest_framework import views
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from . import models,serializers
from django.conf import settings
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework import exceptions
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.shortcuts import redirect
# from django.http import HttpResponsePermanentRedirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import LogoutSerializer
from .permissions import UserIsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import parsers
from rest_framework import mixins
from rest_framework import generics

"""
4 views needed
- Google login 
- user profile list/get read only
- profile update only owner
- logout
"""

# class LoginAPIView(generics.GenericAPIView):
#     authentication_classes = [] # disable authentication
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = serializers.LoginSerializer
#     def post(self, request):
#         serialier = self.serializer_class(data=request.data)
#         serialier.is_valid(raise_exception=True)

#         return Response(serialier.data,status=status.HTTP_200_OK)

class GoogleLogin(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client


class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    TODO:not needed?
    """
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = "id"

class OwnProfileListRetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                                          mixins.ListModelMixin,
                                          mixins.UpdateModelMixin,
                                          viewsets.GenericViewSet):
    """
    for your own profile
    """
    queryset = models.Profile.objects.all()
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (permissions.IsAuthenticated,
                          UserIsOwnerOrReadOnly,
                          )
    serializer_class = serializers.ProfileSerializer
    """for img uplaod"""
    parser_classes = [parsers.MultiPartParser,
                      parsers.FormParser,]
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
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
   

class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)