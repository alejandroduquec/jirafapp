"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from jirafapp.utils.models import JirafaModel


class Province(models.Model):
    """Provinces model."""

    name = models.CharField(
        'Province Name',
        max_length=250,
    )
    slug_name = models.SlugField(
        max_length=40,
        unique=True
    )

    class Meta:
        """Meta class."""

        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        """Return province name."""
        return self.name


class User(JirafaModel, AbstractUser):
    """User model.

    Extend from Django abstract user, change the username field to email
    and add some extra info.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exist',
        }
    )
    
    code = models.CharField(
        'Pin Code',
        max_length=500,
    )

    province = models.ForeignKey(
        'users.Province',
        on_delete=models.CASCADE,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    class Meta:
        """Meta class."""

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username