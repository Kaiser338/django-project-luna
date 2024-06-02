from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import HydroponicSystemSerializer, MeasurementSerializer

hydroponic_system_list_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
        openapi.Parameter('label', openapi.IN_QUERY, description="Filter by label", type=openapi.TYPE_STRING),
        openapi.Parameter('description', openapi.IN_QUERY, description="Filter by description", type=openapi.TYPE_STRING),
        openapi.Parameter('created_at', openapi.IN_QUERY, description="Filter by created_at", type=openapi.TYPE_STRING),
        openapi.Parameter('updated_at', openapi.IN_QUERY, description="Filter by updated_at", type=openapi.TYPE_STRING),
        openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by created_at or updated_at", type=openapi.TYPE_STRING)
    ],
    responses={200: HydroponicSystemSerializer(many=True)},
    security=[{'Bearer': []}]
)

measurement_list_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('system', openapi.IN_QUERY, description="Filter by system", type=openapi.TYPE_INTEGER),
        openapi.Parameter('created_at', openapi.IN_QUERY, description="Filter by created_at", type=openapi.TYPE_STRING),
        openapi.Parameter('pH', openapi.IN_QUERY, description="Filter by pH", type=openapi.TYPE_NUMBER),
        openapi.Parameter('water_temperature', openapi.IN_QUERY, description="Filter by water_temperature", type=openapi.TYPE_NUMBER),
        openapi.Parameter('TDS', openapi.IN_QUERY, description="Filter by TDS", type=openapi.TYPE_NUMBER),
        openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by created_at, pH, water_temperature, or TDS", type=openapi.TYPE_STRING)
    ],
    responses={200: MeasurementSerializer(many=True)},
    security=[{'Bearer': []}]
)