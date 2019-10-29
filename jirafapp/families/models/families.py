"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from jirafapp.utils.models import JirafaModel


class Family(JirafaModel):
    """Family model."""

    members = models.ManyToManyField('families.kid')
    owner = models.ForeignKey(
    'users.User',
    on_delete=models.CASCADE)

    class Meta:
        """Meta class."""

        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'

    def __str__(self):
        """Return province name."""
        return self.owner


class kid(JirafaModel):
    """Kid model.
    """

    gender = models.CharField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exist',
        }
    )
    
    name = models.CharField(
        'Pin Code',
        max_length=500,
    )

    birthdate = models.DateField(
        'Birthdate'
    )
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