from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('customer_app.urls')),
    path('driver/', include('driver_app.urls')),
]
