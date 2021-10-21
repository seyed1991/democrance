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
        admin_user = User.objects.get(id=1)
        self.client.force_login(admin_user)
        response = self.client.post(url, {'customer_id': 1, 'type': 'personal-accident', }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Policy.objects.count(), 1)
        policy = Policy.objects.get()
        self.assertEqual(policy.customer_id, 1)
        self.assertEqual(policy.policy_type, Policy.PolicyTypes.personal_accident)
        self.assertEqual(policy.state, Policy.StateChoices.new)
        self.assertEqual(
            PolicyHistory.objects.filter(policy=policy, action=PolicyHistory.ActionTypes.creation).count(), 1
        )

    def test_quote_acceptance(self):
        """
        Test quote getting accepted.
        """
        url = '/api/v1/quote/'
        admin_user = User.objects.get(id=1)
        self.client.force_login(admin_user)
        quote = Policy(
            policy_type=Policy.PolicyTypes.personal_accident,
            customer=admin_user
        )
        quote.save()
        response = self.client.post(url, {'quote_id': 1, 'status': 'accepted', }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Policy.objects.count(), 1)
        policy = Policy.objects.get()
        self.assertEqual(policy.customer_id, 1)
        self.assertEqual(policy.policy_type, Policy.PolicyTypes.personal_accident)
        self.assertEqual(policy.state, Policy.StateChoices.accepted)
        self.assertEqual(
            PolicyHistory.objects.filter(policy=policy, action=PolicyHistory.ActionTypes.creation).count(), 1
        )
        self.assertEqual(
            PolicyHistory.objects.filter(policy=policy, action=PolicyHistory.ActionTypes.quotation).count(), 1
        )

    def test_policy_activation(self):
        """
        Test quote getting accepted.
        """
        url = '/api/v1/quote/'
        admin_user = User.objects.get(id=1)
        self.client.force_login(admin_user)
        quote = Policy(
            policy_type=Policy.PolicyTypes.personal_accident,
            customer=admin_user
        )
        quote.save()
        response = self.client.post(url, {'quote_id': 1, 'status': 'accepted'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, {'quote_id': 1, 'status': 'active'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Policy.objects.count(), 1)
        policy = Policy.objects.get()
        self.assertEqual(policy.customer_id, 1)
        self.assertEqual(policy.policy_type, Policy.PolicyTypes.personal_accident)
        self.assertEqual(policy.state, Policy.StateChoices.active)
        self.assertEqual(
            PolicyHistory.objects.filter(policy=policy, action=PolicyHistory.ActionTypes.creation).count(), 1
        )
        self.assertEqual(
            PolicyHistory.objects.filter(policy=policy, action=PolicyHistory.ActionTypes.quotation).count(), 1
        )
        self.assertEqual(
            PolicyHistory.objects.filter(policy=policy, action=PolicyHistory.ActionTypes.activation).count(), 1
        )
