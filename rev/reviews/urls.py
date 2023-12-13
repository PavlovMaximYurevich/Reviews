from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet, OrganizationViewSet

router = DefaultRouter()

router.register('organizations', OrganizationViewSet)
router.register(
    r'organizations/(?P<org_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

urlpatterns = [
    path('', include(router.urls)),
]
