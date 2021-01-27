from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@admin.com",
            password="adminadmin"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user1@user1.com",
            password="user1"
        )

    def test_users_listed(self):
        """test that users are listed on user page"""
        url = reverse('admin:account_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        
    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:account_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        
    def test_create_user_page(self):
        url = reverse('admin:account_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
