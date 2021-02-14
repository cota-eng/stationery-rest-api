from .test_setup import TestSetUp
from django.contrib.auth import get_user_model
class TestViews(TestSetUp):
    
    def test_cannot_register_with_invalid_data(self):
        res = self.client.post(self.register_url, format="json")
        #  should repair
        # self.assertEqual(res.status_code, 400)
        
    def test_can_register_with_valid_data_(self):
        res = self.client.post(self.register_url,self.user1_data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['email'],self.user1_data['email'])
        # password check

    def test_user_cannnot_login_with_not_verified_email(self):
        """Test that not verified user login, then 401 unauthorized 
        and check not verified"""
        res_register = self.client.post(self.register_url,self.user1_data,format="json")
        email = res_register.data['email']
        user = get_user_model().objects.get(email=email)
        res_login = self.client.post(self.login_url, self.user1_data, format="json")
        self.assertEqual(res_login.status_code, 401)
        self.assertFalse(user.is_verified)

    def test_user_cannnot_login_after_verified_email(self):
        """ Test that  verified user login, then 200 OK """
        res = self.client.post(self.register_url,self.user1_data,format="json")
        email = res.data['email']
        user = get_user_model().objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, self.user1_data, format="json")
        self.assertEqual(res.status_code, 200)
