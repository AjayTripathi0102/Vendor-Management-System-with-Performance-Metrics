from django.db import models
from vendors.models import Vendor
from django.db.models import Count, Avg
from django.utils import timezone

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

    def update_performance_metrics(self):
        # On-Time Delivery Rate
        completed_purchases = PurchaseOrder.objects.filter(vendor=self.vendor, status='completed')
        on_time_deliveries = completed_purchases.filter(delivery_date__lte=timezone.now()).count()
        total_completed_purchases = completed_purchases.count()
        self.vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_purchases) * 100 if total_completed_purchases else 0

        # Quality Rating Average
        completed_purchases_with_rating = completed_purchases.exclude(quality_rating__isnull=True)
        self.vendor.quality_rating_avg = completed_purchases_with_rating.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0

        # Average Response Time
        acknowledged_purchases = completed_purchases.exclude(acknowledgment_date__isnull=True)
        response_times = (acknowledged_purchases.values_list('acknowledgment_date', flat=True) - acknowledged_purchases.values_list('issue_date', flat=True)).total_seconds()
        self.vendor.average_response_time = response_times.mean() if response_times else 0

        # Fulfilment Rate
        successful_purchases = completed_purchases.filter(status='completed')
        self.vendor.fulfillment_rate = (successful_purchases.count() / total_completed_purchases) * 100 if total_completed_purchases else 0

        self.vendor.save()
