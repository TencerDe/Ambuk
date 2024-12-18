from django.contrib import admin
from .models import Driver, DriverProfile

# Register your models here.

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'vehicle_number', 'is_available')

