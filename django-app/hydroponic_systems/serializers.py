from rest_framework import serializers
from .models import HydroponicSystem, Measurement

class HydroponicSystemSerializer(serializers.ModelSerializer):
    """
    Serializer for HydroponicSystem model.
    """
    class Meta:
        model = HydroponicSystem
        fields = ['id', 'owner', 'name', 'label', 'description', 'created_at', 'updated_at']

class MeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for Measurement model.
    """
    class Meta:
        model = Measurement
        fields = ['id', 'system', 'created_at', 'pH', 'water_temperature', 'TDS']

    def validate_pH(self, value):
        """
        Validation for pH field.
        """
        if value < 0 or value > 14:
            raise serializers.ValidationError("pH must be between 0 and 14")
        return value

    def validate_water_temperature(self, value):
        """
        Validation for water_temperature field.
        """
        if value < 0 or value > 100:
            raise serializers.ValidationError("Water temperature must be between 0 and 100 °C")
        return value

    def validate_TDS(self, value):
        """
        Validation for TDS field.
        """
        if value < 0:
            raise serializers.ValidationError("TDS must be a positive value")
        return value
