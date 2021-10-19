import random
import unicodedata

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        """
        Creates and saves a User with the given data.
        """
        for field in User.REQUIRED_FIELDS:
            if not kwargs.get(field):
                raise ValueError(f'Users must have a/an {field}')

        user = self.model(
            username=self.normalize_username(kwargs['username']),
            first_name=kwargs['first_name'],
            last_name=kwargs['last_name'],
            date_of_birth=kwargs['date_of_birth'],
        )

        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        """
        Creates and saves a superuser with the given data.
        """
        user = self.create_user(**kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user

    @classmethod
    def normalize_username(cls, username):
        username = unicodedata.normalize('NFKC', username) if isinstance(username, str) else username
        return username.lower().replace(' ', '_')  # TODO: can be improved to match username validator regex


class User(AbstractBaseUser):
    username = models.CharField(_('username'), max_length=150, unique=True, validators=[UnicodeUsernameValidator()])
    first_name = models.CharField(_('first name'), max_length=150, db_index=True)
    last_name = models.CharField(_('last name'), max_length=150, db_index=True)
    date_of_birth = models.DateField(db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin user'))

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    class Meta:
        # basically users and customers are the same, verbose_name is used to fulfil task requirements
        verbose_name = "customer"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """specific permission"""
        return True

    def has_module_perms(self, app_label):
        """permissions to view the app `app_label`"""
        return True

    @property
    def is_staff(self):
        """Admin panel access"""
        return self.is_admin

    @classmethod
    def generate_username(cls, data):
        """
        Since we don't have username field when creating customers, and customers need to be able to be authenticated to
         create `Quote` for policies, this method is used to generate username for customers.
        :param data:
        :return generated username:
        """
        username = data.get('username')
        if not username:
            username = UserManager.normalize_username(f'{data["last_name"]}_{data["first_name"]}')
        while cls.objects.filter(username=username).exists():
            username = f'{username}_{random.randint(100, 999)}'
        return username

    @classmethod
    def generate_password(cls, data):
        """
        Since we don't have password field when creating customers, and customers need to be able to be authenticated to
        create `Quote` for policies, this method is used to generate password for customers. The generated password is
        based on `date_of_birth` for simplicity, but in production in can be improved.
        :param data:
        :return generated password:
        """
        password = data.get('password')
        if not password:
            password = data["date_of_birth"].strftime('%Y%m%d')  # simple generated password for test purpose
        return password

