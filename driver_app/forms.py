from django import forms
from .models import DriverProfile

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['phone_number', 'vehicle_number', 'is_available', 'location', 'driver_rating']
