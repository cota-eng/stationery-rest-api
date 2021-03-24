from django.contrib.auth import get_user_model
from django.test import TestCase

class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testuserpass"
        )
        self.assertEqual(user.username,"testuser")
        self.assertEqual(user.email,"testuser@example.com")
        self.assertEqual(user.password, "testuserpass")
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.is_staff)

    def test_create_super_user(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="testadmin", email="testadmin@example.com", password="testadminpass"
        )
        self.assertEqual(user.username,"testadmin")
        self.assertEqual(user.email,"testadmin@example.com")
        self.assertEqual(user.password, "testadminpass")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)