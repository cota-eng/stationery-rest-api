from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('account:register')
        self.login_url = reverse('account:login')
        self.user1_invalid_data = {
            'email': '',
            'password':'',
        }
        self.user1_data = {
            'email': 'user1@example.com',
            'password':'user1password',
        }

        return super().setUp()
