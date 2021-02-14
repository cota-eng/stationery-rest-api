# from rest_framework import serializers
# from . import google_auth,register
# import environ
# from rest_framework import exceptions
# from account import models

# env = environ.Env()
# env.read_env('.env')


# class GoogleAuthSerialier(serializers.ModelSerializer):
#     auth_token = serializers.CharField()
#     class Meta:
#         model = models.User
#         fields = ('auth_token',)
        
#     def validate_auth_token(self, auth_token):
#         user_data = google_auth.Google.validate(auth_token)
#         try:
#             user_data['sub']
#         except:
#             raise serializers.ValidationError(
#             'token is invalid'
#         )

#         if user_data['aud'] != env.get_value('GOOGLE_CLIENT_ID'):
#             raise exceptions.AuthenticationFailed('invalid')
#         print(user_data)
#         user_id = user_data['sub']
#         email = user_data['email']
#         # name = user_data['name'] 
#         provider = 'google'
        
#         return register.register_social_user(
#             provider=provider, user_id=user_id,
#             email=email,
#             # name=name
#         )
