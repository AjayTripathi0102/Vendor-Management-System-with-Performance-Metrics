from django.urls import path
from .views import PurchaseOrderListCreate, PurchaseOrderRetrieveUpdateDestroy, AcknowledgePurchaseOrder

urlpatterns = [
    path('', PurchaseOrderListCreate.as_view()),
    path('<int:pk>/', PurchaseOrderRetrieveUpdateDestroy.as_view()),
    path('<int:pk>/acknowledge/', AcknowledgePurchaseOrder.as_view()),
]
