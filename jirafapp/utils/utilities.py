"""Utilities Jirafapp."""

# Django
from django.core.mail import send_mail

# Utilities
from random import randint


def send_email(user, message):
    """Send email to specific user."""
    if user.email:
        status = send_mail(
            'Recuperar pin.',
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