from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MenuItem, Order, UserObject, OrderItem
from decimal import Decimal
from rest_framework.test import APIClient
import unittest

SKIP_OLD_TESTS = False

class RegisterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse('sign_up')
        cls.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            name="testuser", password="testpass"
        )
        
    def setUp(self):
        self.client = Client()
        self.existing_user_data = {
            "name": "testuser",
            "password": "testpass",
            "email": "testuser@example.com",
        }

        self.valid_user_data = {
            "name": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
        }

        self.not_valid_user_data = {
            "name": "xaa",
            "password": "z",
            "email": "newuser.com",
        }

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_valid_data_registe(self):
        #User created sucesfully
        response = self.client.post(self.register_url, self.valid_user_data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(UserObject.objects.filter(email=self.valid_user_data['email']).exists())


    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_user_existing_register_fail(self):
        #User already in db / email taken
        response = self.client.post(self.register_url, self.existing_user_data)
        self.assertEqual(response.status_code, 400)
        

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_not_valid_data_register_fail(self):
        #not valid credentials

        response = self.client.post(self.register_url, self.not_valid_user_data)
        self.assertEqual(response.status_code, 400)



class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse('sign_in')
        cls.user = get_user_model().objects.create_user(
            email = "testuser@example.com",
            name="testuser", 
            password="testpass"
        )
        
    def setUp(self):
        self.client = Client()
        self.existing_user_data = {
            "name": "testuser",
            "password": "testpass",
            "email": "testuser@example.com",
        }

        self.not_existing_user_data = {
            "name": "testuser2",
            "password": "testpass2",
            "email": "testuser2@example.com",
        }

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_login_sucess(self):
        response = self.client.post(self.login_url, {
            'email': self.existing_user_data['email'],
            'password': self.existing_user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_login_fail(self):
        response = self.client.post(self.login_url, {
            'email': self.not_existing_user_data['email'],
            'password': self.not_existing_user_data['password']
        })
        self.assertEqual(response.status_code, 401)


class MenuItemTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.menu_url = reverse('menu')
        cls.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            name='mike'
        )

        cls.normal_user = get_user_model().objects.create_user(
            email="testuser@example.com",
            name="testuser", 
            password="testpass"
        )
        
    def setUp(self):
        self.client = APIClient()
        self.existing_menu_item = MenuItem.objects.create(
            name='Test Pasta',
            description='Delicious test pasta',
            price='10.99',
            category='pasta'
        )

        self.valid_menu_item_data = {
            'name': 'Test Pizza',
            'description': 'Delicious test pizza',
            'price': '10.99',
            'category': 'pizza'
        }

        self.not_valid_menu_item_data = {
            'name': 'Test Pizza',
            'description': 'Delicious test pizza',
            'price': '10.99',
            'category': 'invalid_category'
        }

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_get_menu_items(self):
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_access_denied_fail(self):
        # Test unauthorized access (not logged in)
        response = self.client.post(self.menu_url, self.valid_menu_item_data)
        self.assertEqual(response.status_code, 401)

        response = self.client.put(f"{self.menu_url}{self.existing_menu_item.id}", self.valid_menu_item_data)
        self.assertEqual(response.status_code, 401)

        response = self.client.delete(f"{self.menu_url}{self.existing_menu_item.id}")
        self.assertEqual(response.status_code, 401)

        # Test forbidden access (normal user)
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.menu_url, self.valid_menu_item_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.put(f"{self.menu_url}{self.existing_menu_item.id}", self.valid_menu_item_data)
        self.assertEqual(response.status_code, 403)

        response = self.client.delete(f"{self.menu_url}{self.existing_menu_item.id}")
        self.assertEqual(response.status_code, 403)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_CRUD_pass(self):
        self.client.force_authenticate(user=self.admin_user)
        
        # Test Create
        response = self.client.post(self.menu_url, self.valid_menu_item_data)
        self.assertEqual(response.status_code, 201)
        created_id = response.data['id']

        # Test Update
        updated_data = self.valid_menu_item_data.copy()
        updated_data['name'] = 'Updated Pizza'
        response = self.client.put(
            f"{self.menu_url}{created_id}",
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Pizza')

        # Test Delete
        response = self.client.delete(f"{self.menu_url}{created_id}")
        self.assertEqual(response.status_code, 204)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_CRUD_fail(self):
        self.client.force_authenticate(user=self.admin_user)
        
        # Test Create with invalid data
        response = self.client.post(self.menu_url, self.not_valid_menu_item_data)
        self.assertEqual(response.status_code, 400)

        # Test Update with invalid data
        response = self.client.put(
            f"{self.menu_url}{self.existing_menu_item.id}",
            self.not_valid_menu_item_data,
            format='json'
        )
        self.assertEqual(response.status_code, 400)

        # Test Delete with invalid ID
        response = self.client.delete(f"{self.menu_url}")
        self.assertEqual(response.status_code, 400)




class UserEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_url = reverse('user')
        cls.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            name="testuser",
            password="testpass",
            delivery_address="Test Address 123",
            phone_number="123456789"
        )
        
    def setUp(self):
        self.client = APIClient()
        self.valid_user_data = {
            "name": "Updated User",
            "delivery_address": "New Address 456",
            "phone_number": "987654321"
        }

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_get_user_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.user.email)

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_update_user_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            self.user_url,
            self.valid_user_data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated User')

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_deactivate_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.user_url)
        self.assertEqual(response.status_code, 200)
        
        # Verify user is deactivated
        user = get_user_model().objects.get(email=self.user.email)
        self.assertFalse(user.is_active)




class OrdersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.orders_url = reverse('order')
        
        cls.normal_user = get_user_model().objects.create_user(
            email="customer@example.com",
            name="customer",
            password="testpass"
        )

        cls.menu_item = MenuItem.objects.create(
            name='Test Pizza',
            description='Delicious test pizza',
            price='10.99',
            category='pizza'
        )
        
    def setUp(self):
        self.client = APIClient()
        self.valid_order_data = {
            'customer_name': 'Test Customer',
            'customer_email': 'customer@example.com',
            'customer_phone': '123456789',
            'delivery_address': 'Test Address 123',
            'items': [{
                'menu_item': self.menu_item.id,
                'quantity': 2
            }]
        }
        
        # Create a test order
        self.existing_order = Order.objects.create(
            customer_name='Existing Customer',
            customer_email='customer@example.com',
            customer_phone='123456789',
            delivery_address='Existing Address 123',
            status='pending'
        )
        
        # Add items to existing order
        OrderItem.objects.create(
            order=self.existing_order,
            menu_item=self.menu_item,
            quantity=1
        )
        self.existing_order.calculate_total()


    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_create_order(self):
        response = self.client.post(
            self.orders_url,
            self.valid_order_data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('redirectUri', response.data)
        self.assertIn('orderId', response.data)


    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")    
    def test_get_order_details_authenticated(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(
            f"{self.orders_url}{self.existing_order.order_number_uuid}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer_email'], 'customer@example.com')

    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_get_order_details_unauthenticated(self):
        response = self.client.get(
            f"{self.orders_url}{self.existing_order.order_number_uuid}",
            {'email': 'customer@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer_email'], 'customer@example.com')


    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_check_payment_status_fail(self):
        response = self.client.get(
            f"{self.orders_url}{self.existing_order.order_number_uuid}",
            {
                'check_payment': 'true',
                'email': 'customer@example.com'
            }
        )
        self.assertEqual(response.status_code, 400) 



    @unittest.skipIf(SKIP_OLD_TESTS, "Skipping old tests")
    def test_check_payment_status_success(self):
        self.existing_order.payu_order_id = 'TEST_PAYU_ORDER_123'
        self.existing_order.payment_status = 'confirmed' 
        self.existing_order.save()

        response = self.client.get(
            f"{self.orders_url}{self.existing_order.order_number_uuid}",
            {
                'check_payment': 'true',
                'email': 'customer@example.com'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['payuStatus'], 'confirmed')
        self.assertEqual(response.data['orderNumber'], self.existing_order.order_number_uuid)





