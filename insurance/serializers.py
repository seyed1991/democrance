from insurance.models import Policy
from rest_framework import serializers


class PolicySerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_policy_type_display')
    status = serializers.CharField(source='get_state_display')

    class Meta:
        model = Policy
        fields = '__all__'
