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
        data = {'request':request,'data':request.data}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        

class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        pass 