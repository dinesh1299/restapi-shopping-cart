from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.api.views import RegisterUser
from rest_framework import status
from rest_framework.authtoken.models import Token

class RegisterUserTest(APITestCase):

    def test_resister(self):
        data = {
            'username':'test_user',
            'email':'test@gmail.com',
            'password':'Pass@123',
            'password2':'Pass@123'
        }

        url = reverse('register_user')

        response = self.client.post(url,data)
        self.assertEqual(response.status_code, 200)


class LoginTestcase(APITestCase):

    def setUp(self):
        User.objects.create_user(username='test_user',password='Pass@123')

    def test_login(self):
        url = reverse('login')
        response = self.client.post(url,dict(username='test_user',password='Pass@123'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse('logout_user')
        token = Token.objects.get(user__username = 'test_user')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)


