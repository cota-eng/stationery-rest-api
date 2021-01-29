from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from . import serializers
from . import utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            created_user = models.User.objects.get(email=serializer.data['email'])
            token = RefreshToken.for_user(created_user).access_token
            current_site = get_current_site(request).domain
            reverse_link = reverse('account:email-veryfy')
            absolute_url = f'http://{current_site}/{reverse_link}?token={token}'

            email_body = f'Hi,there!your mail is {created_user.email}\n please click this url for verifing your account! \n {absolute_url}'

            data = {
                'email_subject': 'verify',
                'email_body': email_body,
                'email_to': created_user.email,
                }
            
            utils.Util.send_email(data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    
    def perform_create(self, serializer):
        return serializer.save(user_profile=self.request.user)

class EmailVerifyView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer
    def get(self, request):
        pass