from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('book/', views.booking_view, name='book'),
    path('booking-status/', views.booking_status, name='booking_status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update/', views.update_details, name='update_details'),
    path('booking-history/', views.booking_history_view, name='booking_history'),
]
