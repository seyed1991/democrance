from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from insurance.models import Policy, PolicyHistory


class PolicyProcessTests(APITestCase):
    fixtures = ["admin_user.json"]

    def test_quote_creation(self):
        """
        Test quote creation.
        """
        url = '/api/v1/quote/'
        data = {
            'customer_id': 1,
            'type': 'personal-accident',
        }
        admin_user = User.objects.get(id=1)
        self.client.force_login(admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Policy.objects.count(), 1)  # admin user already exists
        policy = Policy.objects.get()
        self.assertEqual(policy.customer_id, 1)
        self.assertEqual(policy.policy_type, Policy.PolicyTypes.personal_accident)
        self.assertEqual(policy.state, Policy.StateChoices.new)
        self.assertEqual(
            PolicyHistory.objects.filter(policy=policy, action=PolicyHistory.ActionTypes.creation).count(), 1
        )
