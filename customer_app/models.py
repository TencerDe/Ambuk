from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    preferred_hospital = models.CharField(max_length=100)
    health_details = models.TextField()

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    preferred_hospital = models.CharField(max_length=100)
    pickup_address = models.TextField()
    destination = models.CharField(max_length=100)
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    destination = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Booking for {self.customer.user.username}"
