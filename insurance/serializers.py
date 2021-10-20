from insurance.models import Policy, PolicyHistory
from rest_framework import serializers


class PolicySerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_policy_type_display')
    status = serializers.CharField(source='get_state_display')

    class Meta:
        model = Policy
        fields = '__all__'


class PolicyHistorySerializer(serializers.ModelSerializer):
    action = serializers.CharField(source='get_action_display')
    policy = serializers.StringRelatedField()

    class Meta:
        model = PolicyHistory
        fields = '__all__'
