"""Utilities Jirafapp."""

# Django
from django.core.mail import send_mail


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