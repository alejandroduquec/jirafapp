"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.validators import UniqueValidator
from django.utils import timezone

# Utils
from jirafapp.utils.models import JirafaModel

GENDER_CHOICES = [
        ('M', 'M'),
        ('F', 'F'),
    ]


class Kid(JirafaModel):
    """Kid model.
    
    A kid is a member of family."""

    parent = models.ForeignKey('users.user', on_delete=models.CASCADE)

    gender = models.CharField(
        'Gender',
        max_length=2,
        choices=GENDER_CHOICES,
    )

    username = models.SlugField(
        max_length=40,
        unique=True
    )
    
    name = models.CharField(
        'Kid Name',
        max_length=500,
    )

    birthdate = models.DateField(
        'Birthdate'
    )

    is_premature = models.BooleanField(
        'Is premature',
        default=False
    )

    premature_weaks = models.CharField(
        'Premature weaks',
        null=True,
        blank=True,
        max_length=10,
    )

    class Meta:
        """Meta class."""

        verbose_name = 'Niño'
        verbose_name_plural = 'Niños'

    def __str__(self):
        """Return name."""
        return self.name

    @property
    def age_in_months(self):
        """Check user has active profile."""
        # TODO: check premature data
        age = (timezone.localdate() - self.birthdate).days / 30.4
        return int(age)


class KidHeight(JirafaModel):
    """Kid's heights data model."""

    kid = models.ForeignKey('families.kid', on_delete=models.CASCADE)

    height = models.CharField(
        'Height',
        max_length=10,
    )

    age_height = models.CharField(
        'Age height',
        max_length=10,
        help_text='Age in months at measurement moment.'
    )

    percentile_oms = models.CharField(
        'Percentile Oms',
        max_length=10,
    )
    percentile_sap = models.CharField(
        'Percentile Sap',
        max_length=10,
    )

    date_height = models.DateField(
        'Date Heigth'
    )

    class Meta:
        """Meta class."""

        verbose_name = 'Altura Niño'
        verbose_name_plural = 'Alturas de los Niños'

    def __str__(self):
        """Return name."""
        return '{}|{}'.format(self.kid, self.height)


