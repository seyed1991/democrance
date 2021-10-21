from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Policy(models.Model):
    class PolicyTypes(models.IntegerChoices):
        personal_accident = 1, 'personal-accident'
        earthquake = 2

    class StateChoices(models.IntegerChoices):
        new = 1
        accepted = 2  # Quoted
        active = 3

    policy_type = models.IntegerField(choices=PolicyTypes.choices, verbose_name=_('Policy Type'), db_index=True)
    premium = models.IntegerField(_('Premium'), default=100)
    cover = models.IntegerField(_('Cover'), default=1000)
    state = models.IntegerField(choices=StateChoices.choices, verbose_name=_('Policy State'), db_index=True,
                                default=StateChoices.new)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='policies',
                                 db_index=True)

    class Meta:
        verbose_name_plural = 'Policies'

    def __str__(self):
        return f'{self.customer} - {self.get_policy_type_display()}'

    @classmethod
    def get_choice_by_label(cls, choices, label):
        return next((item for item in choices if item.label == label), None)


class PolicyHistory(models.Model):

    class ActionTypes(models.IntegerChoices):
        creation = 1
        quotation = 2  # accepted by customer: new -> quote
        activation = 3  # quote -> active

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='history')
    action = models.IntegerField(choices=ActionTypes.choices)
    action_datetime = models.DateTimeField(auto_now=True)

    @property
    def customer(self):
        # this is used for owner permission mixin
        return self.policy.customer


@receiver(models.signals.post_save, sender=Policy, dispatch_uid="add_policy_action_history")
def save_policy_history_handler(sender, instance, created, **kwargs):
    """
    This handler is used to save policy history objects after Policy save.
    """
    action = None
    if created:
        action = PolicyHistory.ActionTypes.creation
    elif instance.state == Policy.StateChoices.accepted:
        action = PolicyHistory.ActionTypes.quotation
    elif instance.state == Policy.StateChoices.active:
        action = PolicyHistory.ActionTypes.activation
    if not action:
        return
    history = PolicyHistory(policy=instance, action=action)
    history.save()
