from django.test import TestCase
from django.contrib.auth import get_user_model
from . import models

def create_sample_user(email="smp@smp.com", password="smplepass"):
    return get_user_model().objects.create_user(email, password)
    
class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test that create sample user"""
        email = "test@test.com"
        password = "testtest"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_with_upper_email_successful(self):
        """Test that create user by using upper email"""
        email = "TEST@TEST.COM"
        password = "testtest"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email.lower())
        
    def test_create_user_with_invalid_email(self):
        email = None
        password = "testtest"
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        
    def test_create_superuser(self):
        """Test that create superuser"""
        email = "admin@admin.com"
        password = "adminadmin"
        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

