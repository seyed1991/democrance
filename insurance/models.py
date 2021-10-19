from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Policy(models.Model):
    class PolicyTypes(models.IntegerChoices):
        PERSONAL_ACCIDENT = 1
        EARTHQUAKE = 2

    class StateChoices(models.IntegerChoices):
        New = 1
        Quoted = 2
        Active = 3

    policy_type = models.IntegerField(choices=PolicyTypes.choices, verbose_name=_('Policy Type'), db_index=True)
    premium = models.IntegerField(_('Premium'))
    cover = models.IntegerField(_('Cover'))
    state = models.IntegerField(choices=StateChoices.choices, verbose_name=_('Policy State'), db_index=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='policies',
                                 db_index=True)

    class Meta:
        verbose_name_plural = 'Policies'
