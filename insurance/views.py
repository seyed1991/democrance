from rest_framework import response, views
from django.http import Http404
from insurance.models import Policy
from insurance.serializers import PolicySerializer
from users.models import User


class ListQuotes(views.APIView):
    """
    View to perform Quote Creation and Manipulations.
    """

    def post(self, request):
        data = request.data
        if data.get('quote_id'):
            quote = Policy.objects.filter(id=data['quote_id']).first()
            if not quote:
                raise Http404
            if quote.state == Policy.StateChoices.new and data.get('status') == 'accepted':
                # quote accepted by customer
                # TODO: authenticate customer and policy ownership
                quote.state = Policy.StateChoices.accepted
                quote.save()
            elif quote.state == Policy.StateChoices.accepted and data.get('status') == 'active':
                # quote paid by customer and become policy
                # TODO: authenticate customer and policy ownership
                # TODO: payment simulation
                quote.state = Policy.StateChoices.active
                quote.save()
        else:
            # create new quote
            customer = User.objects.filter(id=data.get('customer_id')).first()
            if not customer:
                raise Http404
            policy_type = Policy.get_choice_by_name(Policy.PolicyTypes, data.get('type'))
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
