from django.urls import path
from .views import VendorListCreate, VendorRetrieveUpdateDestroy, VendorPerformance

urlpatterns = [
    path('', VendorListCreate.as_view()),
    path('<int:pk>/', VendorRetrieveUpdateDestroy.as_view()),
    path('<int:pk>/performance/', VendorPerformance.as_view()),
]
