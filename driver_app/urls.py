from django.urls import path
from . import views

app_name = 'driver'

urlpatterns = [
    path('profile/', views.driver_profile_view, name='driver_profile'),
    path('create_profile/', views.create_driver_profile, name='create_driver_profile'),
]