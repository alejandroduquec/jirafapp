"""Family urls."""

# Django
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import families as families_views

router = DefaultRouter()

router.register(
    r'users/(?P<username>[a-zA-Z0-9_.-]+)/family',
    families_views.FamiliesViewSet,
    basename='families'
)
router.register(
    r'kids',
    families_views.KidsViewSet,
    basename='kids'
)


urlpatterns = [
    path('', include(router.urls))
]
