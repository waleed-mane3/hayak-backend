"""
HOW TO RUN TESTS:
- Through the command link write 'python manage.py test' to run tests for all apps or 'python manage.py tests app_name'.
- Remember that Test Classes will not create posts to your databese, there will be temporary database.
"""

from django.urls import reverse
from rest_framework import status 
from rest_framework.test import APITestCase
from auth_system.models import CustomUser
from rest_framework.authtoken.models import Token



class RegisterTestCase(APITestCase):
    """
    Test Creating New Client
    """
    def test_register_new_client(self):
        data = {
            "first_name":"Ahmad",
            "last_name":"Mohsen",
            "mobile":"0501386177",
            "email":"client12@hayaksa.com",
            "password": "123_123",
            "password2": "123_123"
        }
        # url = reverse('client_list') # name of the url
        response = self.client.post(reverse('account:client_list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class LoginLogoutTestCase(APITestCase):
    """
    Login & Logout the System
    """

    # To test real data 
    # This method will be run be for our test methods
    def setUp(self):
        # Create user to test
        self.user = CustomUser.objects.create(
            email="client55@hayaksa.com",
            password="123_123_$",
            first_name="omar",
            last_name="abdullah"
            )

    # Login Test 
    def test_login_client(self):
        data = {
            "email":"client55@hayaksa.com",
            "password": "123_123_$"
        }
        url = reverse('login') # Name of the url
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)