from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product, Brand
from django.contrib.auth import get_user_model

# class ProductTests(APITestCase):

#     def test_product_list(self):
#         url = reverse('api:productslist', args=(1,))
#         # Create a brand first here to test 
#         response = self.client.get(url, format='json')
#         print(response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
  