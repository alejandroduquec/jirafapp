"""User model."""

# Django
from django.db import models

# Models
from jirafapp.families.models import GENDER_CHOICES


class OmsMeasurement(models.Model):
    """Oms measurements data."""

    gender = models.CharField(
        'Gender',
        max_length=2,
        choices=GENDER_CHOICES,
    )

    age = models.FloatField('Age kid')

    l_size = models.FloatField('L data', default=1)

    m_size = models.FloatField('M data')

    s_size = models.FloatField('S data')

    class Meta:
        """Meta class."""

        verbose_name = 'OMS measurement'
        verbose_name_plural = 'OMS measurements'

    def __str__(self):
        """Return data."""
        return '{}|{}'.format(self.gender, self.age)


class SAPMeasurement(models.Model):
    """SAP measurements data."""

    gender = models.CharField(
        'Gender',
        max_length=2,
        choices=GENDER_CHOICES,
    )

    age = models.FloatField('Age kid')

    median = models.FloatField('Median')

    standard_desviation = models.FloatField('Standar desviation')

    class Meta:
        """Meta class."""

        verbose_name = 'SAP measurement'
        verbose_name_plural = 'SAP measurements'

    def __str__(self):
        """Return data."""
        return '{}|{}'.format(self.gender, self.age)

