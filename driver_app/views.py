from django.shortcuts import render, redirect, get_object_or_404
from .models import Driver
from .forms import DriverProfileForm
from .models import DriverProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

@login_required
def driver_profile(request):
    driver = DriverProfile.objects.get(user=request.user)  # Get the profile for the logged-in driver
    if request.method == 'POST':
        form = DriverProfileForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_profile')  # Redirect to the same page after saving
    else:
        form = DriverProfileForm(instance=driver)
    
    return render(request, 'driver_app/driver_profile.html', {'form': form})

def driver_profile_view(request):
    try:
        driver_profile = DriverProfile.objects.get(user=request.user)
    except DriverProfile.DoesNotExist:
        driver_profile = None  # Or redirect to another page or create profile

    return render(request, 'driver_app/driver_profile.html', {'driver_profile': driver_profile})

def create_driver_profile(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You could also save additional driver info like vehicle number, etc.
            DriverProfile.objects.create(user=user)
            return redirect('driver:driver_profile')  # Redirect to the profile view
    else:
        form = UserCreationForm()

    return render(request, 'driver_app/create_profile.html', {'form': form})
