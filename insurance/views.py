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
            # update quote information
            pass
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
