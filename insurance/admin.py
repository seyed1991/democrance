from django.contrib import admin
from insurance.models import Policy, PolicyHistory


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('customer', 'state', 'policy_type')
    list_filter = ('policy_type', 'state')


@admin.register(PolicyHistory)
class PolicyHistoryAdmin(admin.ModelAdmin):
    list_display = ('policy', 'action', 'action_datetime')
    list_filter = ('action',)
