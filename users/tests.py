from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class CustomerCreationTests(APITestCase):
    fixtures = ["admin_user.json"]

    def test_create_customer(self):
        """
        Test customer creation.
        """
        url = '/api/v1/create_customer/'
        data = {
            'first_name': 'Damian',
            'last_name': 'Dimmich',
            'dob': '25-06-1991',
        }
        admin_user = User.objects.get(id=1)
        self.client.force_login(admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # admin user already exists
        self.assertEqual(User.objects.get(username='dimmich_damian').first_name, 'Damian')
