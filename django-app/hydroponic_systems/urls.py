from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HydroponicSystemViewSet, MeasurementViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'hydroponic', HydroponicSystemViewSet, basename='hydroponic-system')
router.register(r'measurement', MeasurementViewSet, basename='measurement')

urlpatterns = [
    # API endpoints for hydroponic systems and measurements
    path('', include(router.urls)),

    # Token endpoints for authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
