from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from first_app.api import serializers
from first_app.models import *


class CategoryTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="Pass@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.category = Category.objects.create(name="Clothing")

    def test_category_create(self):
        data = {
            "name": "Clothing"
        }
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_list(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_category_ind(self):
        response = self.client.get(reverse('category-detail', args=(self.category.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="Pass@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.category = Category.objects.create(name="Clothing")
        self.product = Product.objects.create(category=self.category, name="Men T Shirt",
                                price="299")

    def test_product_create(self):
        data = dict(category=self.category, name="Men T Shirt", price="299")
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_productt_ind(self):
        response = self.client.get(reverse('product-detail', args=(self.product.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Men T Shirt')


class RatingTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="Pass@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.category = Category.objects.create(name="Clothing")
        self.product1 = Product.objects.create(category=self.category, name="Men T Shirt",
                                price="299")
        self.product2 = Product.objects.create(category=self.category, name="Men jeans",
                                price="495")
        self.rating = Ratings.objects.create(rating=5, product=self.product1, user=self.user)
    
    def test_rating_create(self):
        data = dict(rating=5, product=self.product1, user=self.user)

        response = self.client.post(reverse('rating-create', args=(self.product2.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ratings.objects.count(), 2)

    def test_rating_create_unauth(self):
        data = dict(rating=5, product=self.product1, user=self.user)

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('rating-create', args=(self.product1.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rating_update(self):
        data = dict(rating=3, product=self.product1, user=self.user)

        response = self.client.put(reverse('rating-detail', args=(self.rating.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rating_list(self):
        response = self.client.get(reverse('rating-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_rating_user(self):
        response = self.client.get('/api/rating_detail?username=' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)