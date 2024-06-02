from django.contrib import admin
from .models import HydroponicSystem, Measurement


@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'label', 'created_at', 'updated_at')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('system', 'created_at', 'pH', 'water_temperature', 'TDS')
