from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Hydroponic API",
        default_version='v1',
        description="API for managing hydroponic systems and measurements",
        terms_of_service="xxx",
        contact=openapi.Contact(email="maciekroll@gmail.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)