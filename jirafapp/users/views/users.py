"""Users views."""

# Django Rest Framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from jirafapp.users.permissions import IsAccountOwner

# Models
from jirafapp.users.models import (
    Province,
    User
)

# Serializer
from jirafapp.users.serializers import (
    ProvinceModelSerializer,
    UserModelSerializer,
    UserLoginSerializer,
    UserSignUpSerializer
)


class ProvinceViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Provinces view.

    List all provinces."""

    permission_classes = [AllowAny]
    queryset = Province.objects.all()
    serializer_class = ProvinceModelSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Handle login and signup.
    """

    queryset = User.objects.all()
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permission based on action."""
        if self.action in ['signup', 'login']:
            permissions = [AllowAny]
        elif self.action in ['retrieve']:
            permissions = [IsAuthenticated, IsAccountOwner]
        return [p() for p in permissions]

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'login':
            return UserLoginSerializer
        if self.action == 'signup':
            return UserSignUpSerializer
        return UserModelSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User signup."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)