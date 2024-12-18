from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    phone_number = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)  # Availability of the driver
    location = models.CharField(max_length=100, blank=True, null=True)  # Driver's current location (optional)
    driver_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)  # Rating out of 5

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_number}"
