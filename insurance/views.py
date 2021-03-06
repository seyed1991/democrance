from rest_framework import response, views, permissions
from rest_framework.decorators import permission_classes
from django.http import Http404
from insurance.models import Policy
from insurance.serializers import PolicySerializer, PolicyHistorySerializer
from users.models import User
from users.permissions import IsAdminOrOwnerPermission


class QuoteList(views.APIView):
    """
    View to create,edit and list quotes.
    """

    # @permission_classes([IsAdminOrOwnerPermission])
    def get(self, request):
        """
        View to list customer quotes.
        """
        customer_id = request.GET.get('customer_id', request.user.id)
        quotes = Policy.objects.filter(customer_id=customer_id).exclude(state=Policy.StateChoices.active)
        policy_type = request.query_params.get('type')
        if policy_type:
            quotes = quotes.filter(policy_type=Policy.get_choice_by_label(Policy.PolicyTypes, policy_type))
        serializer = PolicySerializer(quotes, many=True)
        return response.Response(serializer.data)

    # @permission_classes([permissions.IsAuthenticated])
    def post(self, request):
        """
        View to perform Quote Creation and Manipulations.
        """
        data = request.data
        if data.get('quote_id'):
            quote = Policy.objects.filter(id=data['quote_id']).first()
            if not quote:
                raise Http404
            if quote.state == Policy.StateChoices.new and data.get('status') == 'accepted':
                # quote accepted by customer
                quote.state = Policy.StateChoices.accepted
                quote.save()
            elif quote.state == Policy.StateChoices.accepted and data.get('status') == 'active':
                # quote paid by customer and become policy
                # TODO: payment simulation
                quote.state = Policy.StateChoices.active
                quote.save()
        else:
            # create new quote
            customer = User.objects.filter(id=data.get('customer_id')).first()
            if not customer:
                raise Http404
            policy_type = Policy.get_choice_by_label(Policy.PolicyTypes, data.get('type'))
            if not policy_type:
                raise Http404
            quote = Policy(
                customer=customer,
                policy_type=policy_type,
                premium=data.get('premium', 100),
                cover=data.get('cover', 1000)
            )
            quote.save()
        serializer = PolicySerializer(quote)
        return response.Response(serializer.data)


class PolicyList(views.APIView):
    """
    View to list customer's policies.
    """

    # @permission_classes([IsAdminOrOwnerPermission])
    def get(self, request):
        customer_id = request.GET.get('customer_id', request.user.id)
        policies = Policy.objects.filter(
            state=Policy.StateChoices.active,
            customer_id=customer_id
        )
        policy_type = request.query_params.get('type')
        if policy_type:
            policies = policies.filter(policy_type=Policy.get_choice_by_label(Policy.PolicyTypes, policy_type))
        serializer = PolicySerializer(policies, many=True)
        return response.Response(serializer.data)


class PolicyDetail(views.APIView):
    """
    View to list customer's policies.
    """

    # @permission_classes([IsAdminOrOwnerPermission])
    def get(self, request, policy_id):
        policy = Policy.objects.filter(id=policy_id, state=Policy.StateChoices.active).first()
        if not policy:
            raise Http404
        serializer = PolicySerializer(policy)
        return response.Response(serializer.data)


class PolicyHistory(views.APIView):
    """
    View to list policy's history.
    """

    # @permission_classes([IsAdminOrOwnerPermission])
    def get(self, request, policy_id):
        policy = Policy.objects.filter(id=policy_id).first()
        if not policy:
            raise Http404
        serializer = PolicyHistorySerializer(policy.history, many=True)
        return response.Response(serializer.data)
