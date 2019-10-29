"""Families views."""

# Django Rest Framework
from rest_framework import status, viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from jirafapp.families.permissions import IsParent
from jirafapp.users.permissions import IsAccountOwner

# Models
from jirafapp.families.models import (
    Kid
)
from jirafapp.users.models import User

# Serializer
from jirafapp.families.serializers import (
    KidModelSerializer,
    CreateKidModelSerializer
)


class FamiliesViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """Families view."""

    permission_classes = [IsParent, IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the user exist"""
        username = kwargs['username']
        self.user = get_object_or_404(User, username=username)
        return super(FamiliesViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return user family."""
        return Kid.objects.filter(
            parent=self.user
        ).order_by('created')
    
    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'list':
            return KidModelSerializer
        elif self.action == 'create':
            return CreateKidModelSerializer
        return KidModelSerializer

    def create(self, request, *args, **kwargs):
        """Handle kid creation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kid = serializer.save()
        data = KidModelSerializer(kid).data
        return Response(data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        """Get Family members."""
        # TODO: for any reason has_permissions method have an issue resolve it
        if self.user != request.user:
            data = {"detail": "You do not have permission to perform this action."}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class KidsViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Kids Viewset."""
    
    queryset = Kid.objects.all()
    lookup_field = 'username'
    serializer_class = KidModelSerializer
    permission_classes = [IsParent]






