"""Users urls."""

# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views

router = DefaultRouter()
router.register(r'provinces', user_views.ProvinceViewSet, basename='provinces')

urlpatterns = [
    path('', include(router.urls))
]
