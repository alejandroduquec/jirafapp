"""Users views."""

# Django Rest Framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response


# Models
from jirafapp.users.models import Province

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

# Serializer
from jirafapp.users.serializers import ProvinceSerializer


class ProvinceViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Provinces view.

    List all provinces."""

    permission_classes = [AllowAny]
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
