from rest_framework.permissions import BasePermission

class IsMeasurementOwner(BasePermission):
    """
    Custom permission to only allow owners of the measurement to view, update or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.system.owner == request.user
