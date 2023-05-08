# from django.urls import reverse
# from django.urls import reverse
# from Accounts.models import User
# from rest_framework.test import APITestCase
# from rest_framework import status
# from .models import Category, Product, ProductImg
# from .serializers import CategorySerializer, ProductSerializer, ProductImgSerializer


# class ProductListTests(APITestCase):
#     def setUp(self):
#         self.url = reverse('shop_app:Product_list')

#         self.user = User.objects.create_superuser(
#             email='testuser@example.com',
#             password='testpassword',
        
#         )
#         self.category = Category.objects.create(title='test category')
#         self.product = Product.objects.create(
#             name='test product',
#             category=self.category,
#             preview_text='test preview text',
#             detail_text='test detail text',
#             price=9.99,
#             old_price=19.99
#         )
#         self.image = ProductImg.objects.create(
#             product=self.product,
#             mainimage='test_image.jpg'
#         )
#         self.client.force_authenticate(user=self.user)

        
#     def test_get_all_products(self):
#         url = self.url
#         response = self.client.get(url, format='json')
    
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['name'], 'test product')
#         self.assertEqual(response.data[0]['category'], 'test category')
#         self.assertEqual(response.data[0]['preview_text'], 'test preview text')
#         self.assertEqual(response.data[0]['detail_text'], 'test detail text')
#         self.assertEqual(response.data[0]['price'], 9.99)
#         self.assertEqual(response.data[0]['old_price'], 19.99)
#         self.assertEqual(len(response.data[0]['images']), 1)
#         self.assertEqual(response.data[0]['images'][0]['mainimage'], '/media/test_image.jpg')
        

#     def test_create_product(self):
#         self.client.login(email='testuser@example.com', password='testpassword')
#         self.client.force_authenticate(user=self.user)

#         data = {
#             'name': 'new test product',
#             'category': self.category,
#             'preview_text': 'new test preview text',
#             'detail_text': 'new test detail text',
#             'price': 19.99,
#             'old_price': 29.99,
#             'images': [{'mainimage': 'new_test_image.jpg'}]
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Product.objects.count(), 2)
#         self.assertEqual(Product.objects.get(name='new test product').category.title, 'test category')
#         self.assertEqual(ProductImg.objects.count(), 1)



        
#     def test_update_product(self):
#         self.client.login(email='testuser@example.com', password='testpassword')
#         self.client.force_authenticate(user=self.user)
#         url = reverse("shop_app:product_details", args=[self.product.slug])
#         # p=Product.objects.get(name='new test product')
#         data = {
#             'name': 'new test product',
#             'category': self.category,
#             'preview_text': 'new test preview text',
#             'detail_text': 'new test detail text',
#             'price': 19.99,
#             'old_price': 29.99,
#             'slug':'new-test-product',

#         }
#         response = self.client.put(url, data)
#         if response.status_code == status.HTTP_400_BAD_REQUEST:
#             print(response.data['category'])  # prints the validation errors



#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Product.objects.get(slug=self.product.slug).name, data["name"])
#         self.assertEqual(Product.objects.get(id=self.product.id).preview_text, data["preview_text"])
#         self.assertEqual(Product.objects.get(id=self.product.id).detail_text, data["detail_text"])
        
