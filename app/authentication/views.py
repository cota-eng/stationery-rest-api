from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,views
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from . import models,serializers
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from django.utils.encoding import smart_bytes,smart_str, force_str, DjangoUnicodeDecodeError
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


# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import LogoutSerializer

"""
4 views needed
- Google login 
- user profile list/get read only
- profile update only owner
logout
"""

class GoogleLogin(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client

# class MyProfileView(viewsets.ModelViewSet):
#     queryset = models.Profile.objects.all()
#     serializer_class = serializers.ProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#     def get_queryset(self):
#             return self.queryset.filter(user_profile=self.request.user)
# put only ?

class ProfileReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = "id"

from .permissions import UserIsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class ProfileRetrieveUpdateViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated,
                          UserIsOwnerOrReadOnly,
                          )
    serializer_class = serializers.ProfileSerializer
    
    def destroy(self, request, *args, **kwargs):
        """
        delete is invalid
        """
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        list is invalid
        """
        response = {'message': 'list method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """
        psot is invalid
        """
        response = {'message': 'post method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# class UserProfileChangeAPIView(generics.RetrieveAPIView,
#                             #    mixins.DestroyModelMixin,
#                                mixins.UpdateModelMixin):
#     permission_classes = (
#         permissions.IsAuthenticated,
#         UserIsOwnerOrReadOnly,
#     )
#     serializer_class = serializers.ProfileSerializer
#     # parser_classes = (MultiPartParser, FormParser,)

#     def get_object(self):
#         id = self.kwargs["id"]
#         obj = get_object_or_404(get_user_model(), id=id)
#         return obj

#     # def delete(self, request, *args, **kwargs):
#     #     return self.destroy(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

"""
not needed
"""
# class ProfileListView(generics.ListAPIView):
#     queryset = models.Profile.objects.all()
#     serializer_class = serializers.ProfileSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    # def get_queryset(self):
    #     return self.queryset.filter(userProfile=self.request.user)
 
class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)