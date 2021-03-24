from django.contrib.auth import get_user_model
from django.test import TestCase

class CustomUserTests(TestCase):
    fixtures = ["fixtures/master/avatar.json"]
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testuserpass"
        )
        self.assertEqual(user.username,"testuser")
        self.assertEqual(user.email,"testuser@example.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_super_user(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="testadmin", email="testadmin@example.com", password="testadminpass"
        )
        self.assertEqual(user.username,"testadmin")
        self.assertEqual(user.email,"testadmin@example.com")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)