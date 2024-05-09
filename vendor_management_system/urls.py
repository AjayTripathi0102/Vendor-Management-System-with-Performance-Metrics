from django.contrib import admin
from django.urls import path, include
from vendor_management_system.views import index
urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/vendors/', include('vendors.urls')),
    path('api/purchase_orders/', include('purchase_orders.urls')),
]
