"""Users Serializers."""

# Django
from django.contrib.auth import password_validation, authenticate
from django.core.mail import BadHeaderError, send_mail

# Loggin
import logging

# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.conf import settings

# Model
from jirafapp.users.models import (
    Province,
    User
)

# Utils
from jirafapp.utils.utilities import send_email
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class ProvinceModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta serializer."""

        model = Province
        fields = (
            'name',
            'slug_name'
        )


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    province = ProvinceModelSerializer(read_only=True)

    class Meta:
        """Meta serializer."""

        model = User
        fields = (
            'username',
            'first_name',
            'email',
            'province'
        )


class UserLoginSerializer(serializers.Serializer):
    """Users login Serializer.

    Handle login request data.
    """

    email = serializers.EmailField()
    code = serializers.CharField(min_length=3)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['code'])
        if not user:
            raise serializers.ValidationError('Invalid credential')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        # Token is one to one field with user
        token, created = Token.objects.get_or_create(user=self.context.get('user'))
        return self.context['user'], token.key


class UserSignUpSerializer(serializers.Serializer):
    """Users signup serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    code = serializers.CharField(max_length=14, min_length=3)

    # Name
    first_name = serializers.CharField(min_length=1)

    # Province
    province = serializers.SlugField(
        max_length=40,
    )

    def validate_province(self, data):
        """Validate province slugname."""
        try:
            province = Province.objects.get(slug_name=data)
        except Province.DoesNotExist:
            province = None
        if not province:
            raise serializers.ValidationError("province does not exist by slugname.")
        return province

    def validate(self, data):
        """Verify password match."""
        email = data.get('email')
        username = email.split('@')
        # create username by email
        if 'username' not in data:
            data['username'] = username[0]
            if User.objects.filter(username=username[0]).exists():
                raise serializers.ValidationError("User with username {} already exists.".format(username[0]))
        # User does not needs a password only a public pin
        code = data.get('code')
        data['password'] = code

        # Encrypt data
        f = Fernet(settings.KEY_ENCRYPT)
        data['code'] = f.encrypt(code.encode()).decode()
        return data

    def create(self, data):
        """Handle user and profile creation."""
        user = User.objects.create_user(**data)
        token, created = Token.objects.get_or_create(user=user)
        return user, token.key


class RememberCodeSerializer(serializers.Serializer):
    """Reset code Serializer."""

    email = serializers.EmailField()

    def validate_email(self, data):
        """Check email credentials."""
        email = User.objects.filter(email=data)
        if not email:
            raise serializers.ValidationError('Este correo electrónico no es válido.')
        return data
    
    def create(self, data):
        """Handle create method to send reset email."""
        # Send email
        user = User.objects.get(email=data['email'])
        # Decrypt data
        f = Fernet(settings.KEY_ENCRYPT)
        bytes_code = f.decrypt(user.code.encode())
        try:
            send_mail(
                subject='[Jirafapp] Recovery Code',
                message='Hi {}. Remember that your code is {}'.format(
                    user.first_name,
                    bytes_code.decode()),
                from_email='noreply@jirafapp.com',
                recipient_list=[user.email],
                fail_silently=False,
                )
        except BadHeaderError as e:
            logger.error("Error sent email: %s", e)

        return bytes_code.decode()



