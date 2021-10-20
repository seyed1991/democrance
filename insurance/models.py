from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Policy(models.Model):
    class PolicyTypes(models.IntegerChoices):
        personal_accident = 1
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

    @classmethod
    def get_choice_by_name(cls, choices, name):
        return next((item for item in choices if item.name == name), None)
