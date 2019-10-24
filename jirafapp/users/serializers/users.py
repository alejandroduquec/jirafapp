"""Users Serializers."""

# Django
from django.contrib.auth import password_validation, authenticate

# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Model
from jirafapp.users.models import (
    Province
)


class ProvinceSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta serializer."""

        model = Province
        fields = (
            'name',
            'slug_name'
        )