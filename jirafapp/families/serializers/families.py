"""Family Serializers."""

# Django
from django.contrib.auth import password_validation, authenticate
from django.utils import timezone

# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Model
from jirafapp.families.models import (
    Kid,
    KidHeight,
    OmsMeasurement
)

# Utilities
from jirafapp.utils.utilities import (
    random_with_n_digits,
    calcle_percentile_oms,
    calcle_percentile_sap
)

INPUT_FORMATS = ['%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']


class KidModelSerializer(serializers.ModelSerializer):
    """Kid model serializer."""

    class Meta:
        """Meta serializer."""

        model = Kid
        fields = ['gender', 'username', 'name',
                  'birthdate', 'age_in_months',
                  'premature_date', 'is_premature']


class UpdateKidModelSerializer(serializers.ModelSerializer):
    """Update Kid model serializer."""

    birthdate = serializers.DateField(format='%Y-%m-%d', input_formats=INPUT_FORMATS)

    class Meta:
        """Meta serializer."""

        model = Kid
        fields = ['birthdate', 'name']


class KidHeightModelSerializer(serializers.ModelSerializer):
    """Kid model serializer."""

    class Meta:
        """Meta serializer."""

        model = KidHeight
        exclude = ('id', 'created', 'modified', 'kid')


class CreateKidModelSerializer(serializers.ModelSerializer):
    """Create kid Serializer."""

    parent = serializers.HiddenField(default=serializers.CurrentUserDefault())
    birthdate = serializers.DateField(format='%Y-%m-%d', input_formats=INPUT_FORMATS)
    premature_date = serializers.DateField(format='%Y-%m-%d', input_formats=INPUT_FORMATS, required=False)

    class Meta:
        """Meta class."""

        model = Kid
        exclude = ('created', 'modified', 'username')

    def validate_birthdate(self, data):
        """Ensure under than 19 years old."""
        age = (timezone.localdate() - data).days / 365
        if age >= 19:
            raise serializers.ValidationError('Kid must be under 19 years.')
        return data

    def validate(self, data):
        """Create custom username."""
        data['username'] = 'kid_{}_{}{}'.format(
            data['name'][0:2],
            data['gender'][0].lower(),
            random_with_n_digits(5)
        )
        # Ensure premature date when kid is premaute
        if data.get('is_premature', False) and 'premature_date' not in data:
            raise serializers.ValidationError({'premature_date': 'This field is required'})
        return data

    def create(self, data):
        """Handle kid creation."""
        kid = Kid.objects.create(**data)
        return kid


class CreateKidHeightModelSerializer(serializers.ModelSerializer):
    """Create kid's height Serializer."""

    date_height = serializers.DateField(format='%Y-%m-%d', input_formats=INPUT_FORMATS)

    class Meta:
        """Meta class."""

        model = KidHeight
        fields = (
            'height',
            'date_height',
        )

    def validate_height(self, data):
        """Check height value."""
        data = float(data)
        if data < 20:
            raise serializers.ValidationError('The height must be in cms.')
        return data

    def validate_date_height(self, data):
        """Check height date."""
        kid = self.context['kid']
        if data < kid.birthdate:
            raise serializers.ValidationError('measurement must be before the date of birth.')
        return data

    def create(self, data):
        """Handle height creation."""
        kid = self.context['kid']

        # Date measurement
        date_height = data.get('date_height')
        height = data.get('height')

        # Age in months
        age_height = (date_height - kid.birthdate).days / 30.4

        # Age in years
        age_years = int(age_height)/12

        z_oms = calcle_percentile_oms(height, kid, age_years)
        z_sap = calcle_percentile_sap(height, kid, age_years)

        # Data complete
        data['age_height'] = int(age_height)
        data['kid'] = kid
        data['height'] = int(height)
        data['percentile_oms'] = z_oms
        data['percentile_sap'] = z_sap
        kid_height = KidHeight.objects.create(**data)
        return kid_height
