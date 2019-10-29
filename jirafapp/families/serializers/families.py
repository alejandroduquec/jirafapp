"""Family Serializers."""

# Django
from django.contrib.auth import password_validation, authenticate

# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from jirafapp.families.models import (
    Kid
)

# Utilities
from jirafapp.utils.utilities import random_with_n_digits

INPUT_FORMATS = ['%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']


class KidModelSerializer(serializers.ModelSerializer):
    """Kid model serializer."""

    class Meta:
        """Meta serializer."""

        model = Kid
        exclude = ('id', 'created', 'modified', 'parent')


class CreateKidModelSerializer(serializers.ModelSerializer):
    """Create kid Serializer."""

    parent = serializers.HiddenField(default=serializers.CurrentUserDefault())
    birthdate = serializers.DateField(format='%Y-%m-%d', input_formats=INPUT_FORMATS)
    premature_date = serializers.DateField(format='%Y-%m-%d', input_formats=INPUT_FORMATS, required=False)

    class Meta:
        """Meta class."""

        model = Kid
        exclude = ('created', 'modified', 'username')

    def validate(self, data):
        """Create custom username."""
        data['username'] = 'kid_{}_{}{}'.format(
            data['name'][0:2],
            data['gender'][0].lower(),
            random_with_n_digits(5)
        )
        return data

    def create(self, data):
        """Handle kid creation."""
        kid = Kid.objects.create(**data)
        return kid

