"""Utilities Jirafapp."""

# Django
from django.core.mail import send_mail

# Models
from jirafapp.families.models import (
    OmsMeasurement,
    SAPMeasurement
)

# Utilities
from random import randint


def send_email(user, message):
    """Send email to specific user."""
    if user.email:
        status = send_mail(
            'Jirafa App - Tu pin de acceso.',
            message,
            'tech@jirafapp.com',
            [user.email],
            fail_silently=False,
        )


def random_with_n_digits(n):
    """Create random number of n digits."""
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def calcle_percentile_oms(height, kid, age_years):
    """Calcle for oms method."""
    lower = OmsMeasurement.objects.filter(
        gender=kid.gender,
        age__lte=age_years
    ).last()

    greater = OmsMeasurement.objects.filter(
        gender=kid.gender,
        age__gte=age_years
    ).first()

    lower_data = abs(lower.age - age_years)
    greater_data = abs(greater.age - age_years)
    if lower_data < greater_data:
        data_oms = lower
    else:
        data_oms = greater
    # Zscore calcle
    zscore = (((height/data_oms.m_size)**data_oms.l_size) - 1)/(
                data_oms.l_size*data_oms.s_size)

    return round(zscore, 5)


def calcle_percentile_sap(height, kid, age_years):
    """Calcle for sap method."""
    lower = SAPMeasurement.objects.filter(
        gender=kid.gender,
        age__lte=age_years
    ).last()

    greater = SAPMeasurement.objects.filter(
        gender=kid.gender,
        age__gte=age_years
    ).first()

    lower_data = abs(lower.age - age_years)
    greater_data = abs(greater.age - age_years)
    if lower_data < greater_data:
        data_sap = lower
    else:
        data_sap = greater
    # Zscore calcle
    zscore = (height - data_sap.median)/data_sap.standard_desviation

    return round(zscore, 5)
