from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer, Booking
from .forms import BookingForm
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from driver_app.models import DriverProfile

# Create your views here.

def home(request):
    return render(request, 'customer_app/home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return render(request, 'customer_app/signup.html')

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Create the corresponding Customer profile
        customer = Customer(user=user, phone_number=phone_number, address=address)
        customer.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'customer_app/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')  # Check for 'next' parameter
            return redirect(next_url if next_url else 'profile')  # Default to profile if 'next' is absent
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'customer_app/login.html')

@login_required
def profile_view(request):
    if request.user.is_authenticated:
        try:
            # Try fetching the Customer profile
            customer = Customer.objects.get(user=request.user)
            return render(request, 'customer_app/profile.html', {'customer': customer})
        except Customer.DoesNotExist:
            # If Customer profile doesn't exist, try fetching the Driver profile
            try:
                driver = DriverProfile.objects.get(user=request.user)
                return render(request, 'driver_app/driver_profile.html', {'driver': driver})
            except DriverProfile.DoesNotExist:
                # Handle the case if neither profile exists
                return render(request, 'error.html', {'message': 'Profile not found!'})
    else:
        return redirect('login')

@login_required
def booking_view(request):
    # This ensures the form is displayed when the page is loaded
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save the form with the customer
            booking = form.save(commit=False)
            booking.customer = request.user.customer  # Associate the booking with the customer
            booking.save()  # Save the booking
            return redirect('booking_status')  # Redirect to the status page after successful booking
    else:
        form = BookingForm()  # Empty form if not POST request

    return render(request, 'customer_app/booking.html', {'form': form})

@login_required
def booking_status(request):
    if request.method == 'GET':
        customer = request.user.customer 
        bookings = Booking.objects.filter(customer=customer).order_by('-created_at')  # Get bookings of the customer

        context = {
            'bookings': bookings,
        }
        return render(request, 'customer_app/booking_status.html', context)

@login_required
def dashboard(request):
    user = request.user
    # Get the customer instance based on the logged-in user
    customer = Customer.objects.get(user=user)

    return render(request, 'customer_app/dashboard.html', {'customer': customer})

@login_required
def update_details(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    if request.method == 'POST':
        customer.preferred_hospital = request.POST.get('preferred_hospital')
        customer.patient_details = request.POST.get('patient_details')
        customer.save()
        return redirect('dashboard')  # Redirect to dashboard after update

    return render(request, 'customer_app/update_details.html', {'customer': customer})

def book_ambulance(request):
    if request.method == "POST":
        # Your logic to book the ambulance in the database here
        booking = Booking.objects.create(
            customer=request.user,
            ambulance_number=request.POST['ambulance_number'],
            pickup_location=request.POST['pickup_location'],
            destination=request.POST['destination'],
            booking_status='Confirmed',
        )
        return JsonResponse({"status": "success"})
    return render(request, 'book_ambulance.html')

def booking_history_view(request):
    # Fetch the user's booking history from the database
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'booking_history.html', {'bookings': bookings})
