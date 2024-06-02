from django.db import models
from django.contrib.auth.models import User

class HydroponicSystem(models.Model):
    """
    Model representing a hydroponic system.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hydroponic_systems')
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label or self.name

class Measurement(models.Model):
    """
    Model representing a measurement in a hydroponic system.
    """
    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name='measurements')
    created_at = models.DateTimeField(auto_now_add=True)
    pH = models.DecimalField(max_digits=4, decimal_places=2)
    water_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    TDS = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'Measurement at {self.created_at}'
