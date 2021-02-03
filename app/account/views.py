from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,views
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from . import models,serializers,utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.utils.encoding import smart_bytes,smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework import exceptions
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from . import utils
from django.contrib.auth.tokens import PasswordResetTokenGenerator

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
            absolute_url = f'http://{current_site}{reverse_link}?token={token}'

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


class EmailVerifyAPIView(views.APIView):
    serializer_class = serializers.EmailVerifySerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
            user = models.User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error':'not successfully activated'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            

class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    def post(self, request):
        serialier = self.serializer_class(data=request.data)
        serialier.is_valid(raise_exception=True)

        return Response(serialier.data,status=status.HTTP_200_OK)

class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if models.User.objects.filter(email=email).exists():
            user = models.User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            reverse_link = reverse('account:password-reset-confirm',kwargs={'uidb64':uidb64,'token':token})
            absolute_url = f'http://{current_site}{reverse_link}'

            email_body = f'Hi,there! \n please click this url for reset your password! \n {absolute_url}'

            data = {
                'email_subject': 'reset password',
                'email_body': email_body,
                'email_to': user.email,
                }
            
            utils.Util.send_email(data)
        # data = {'request':request,'data':request.data}
        # serializer = self.serializer_class(data=data)
        # serializer.is_valid(raise_exception=True)
            return Response({'success': 'sent you a password reset link!'},
                status=status.HTTP_200_OK)

class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        pass 