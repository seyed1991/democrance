from django.contrib import admin
from insurance.models import Policy


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('customer', 'state', 'policy_type')
    list_filter = ('policy_type', 'state')
