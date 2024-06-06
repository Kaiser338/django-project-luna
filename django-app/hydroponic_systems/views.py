from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from .permissions import IsMeasurementOwner
from .swagger_schemas import hydroponic_system_list_schema, measurement_list_schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on hydroponic systems.

    - List all hydroponic systems owned by the authenticated user.
    - Create a new hydroponic system.
    - Retrieve details of a specific hydroponic system, including the last 10 measurements associated with it.
    - Delete a hydroponic system owned by the authenticated user.
    - Update a specific hydroponic system by the authenticated user.
    """
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'label': ['exact', 'icontains'],
        'description': ['exact', 'icontains'],
        'created_at': ['exact', 'lt', 'lte', 'gt', 'gte'],
        'updated_at': ['exact', 'lt', 'lte', 'gt', 'gte']
    }
    ordering_fields = ['created_at', 'updated_at']


    @hydroponic_system_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request):
        """
        Create a new hydroponic system owned by the authenticated user.

        Request Body:
        {
            "name": "Hydroponic System Name",
            "label": "Optional Label",
            "description": "Optional Description"
        }

        Response Body:
        {
            "id": 1,
            "name": "Hydroponic System Name",
            "label": "Optional Label",
            "description": "Optional Description",
            "created_at": "2024-06-02T12:00:00Z",
            "updated_at": "2024-06-02T12:00:00Z"
        }
        """
        request.data['owner'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        """
        Get a queryset of hydroponic systems owned by the authenticated user.
        Apply default ordering if no ordering parameter is provided.
        """
        queryset = self.queryset.filter(owner=self.request.user)

        if not self.request.query_params.get('ordering'):
            queryset = queryset.order_by('-updated_at')

        return queryset

    def retrieve(self, request, pk=None):
        """
        Retrieve details of a specific hydroponic system, including the last 10 measurements associated with it.

        Query Parameters:
        - num_measurements: int (optional)

        Response Body:
        {
            "id": 1,
            "name": "Hydroponic System Name",
            "label": "Optional Label",
            "description": "Optional Description",
            "created_at": "2024-06-02T12:00:00Z",
            "updated_at": "2024-06-02T12:00:00Z",
            "last_10_measurements": [
                {
                    "id": 1,
                    "system": 1,
                    "created_at": "2024-06-02T12:00:00Z",
                    "pH": 6.5,
                    "water_temperature": 25.5,
                    "TDS": 500
                },
                ...
            ]
        }
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        num_measurements = request.query_params.get('num_measurements', 10)
        try:
            num_measurements = int(num_measurements)
        except ValueError:
            return Response({"error": "num_measurements must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        measurements = instance.get_last_measurements(num_measurements)
        measurement_serializer = MeasurementSerializer(measurements, many=True)
        data['last_measurements'] = measurement_serializer.data

        return Response(data)
    
    def destroy(self, request, pk=None):
        """
        Delete a hydroponic system owned by the authenticated user.
        """
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Hydroponic system deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on measurements associated with hydroponic systems owned by the authenticated user.

    - List all measurements associated with hydroponic systems owned by the authenticated user.
    - Create a new measurement associated with a hydroponic system owned by the authenticated user.
    - Retrieve details of a specific measurement associated with a hydroponic system owned by the authenticated user.
    - Update a specific measurement associated with a hydroponic system owned by the authenticated user.
    - Delete a specific measurement associated with a hydroponic system owned by the authenticated user.
    """
    serializer_class = MeasurementSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'system': ['exact'],
        'created_at': ['exact', 'lt', 'lte', 'gt', 'gte'],
        'pH': ['exact', 'lt', 'lte', 'gt', 'gte'],
        'water_temperature': ['exact', 'lt', 'lte', 'gt', 'gte'],
        'TDS': ['exact', 'lt', 'lte', 'gt', 'gte']
    }
    ordering_fields = ['created_at', 'pH', 'water_temperature', 'TDS']
    permission_classes = [IsAuthenticated, IsMeasurementOwner]

    @measurement_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, pk=None):
        """
        Create a new measurement associated with a hydroponic system owned by the authenticated user.

        Request Body:
        {
            "system": 1,
            "pH": 6.5,
            "water_temperature": 25.5,
            "TDS": 500
        }
        """
        system_id = request.data.get('system')
        system = HydroponicSystem.objects.filter(id=system_id, owner=request.user).first()

        if system:
            system.save()
            return super().create(request)
        else:
            return Response({"error": "You do not have permission to create measurements for this system."}, status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        """
        Get a queryset of measurements associated with hydroponic systems owned by the authenticated user.
        """
        user_systems = HydroponicSystem.objects.filter(owner=self.request.user)
        user_system_ids = user_systems.values_list('id', flat=True)
        queryset = Measurement.objects.filter(system_id__in=user_system_ids)

        if not self.request.query_params.get('ordering'):
            queryset = queryset.order_by('-created_at')

        return queryset