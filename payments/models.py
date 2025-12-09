from django.db import models
from orders.models import Order
# Create your models here.
class PaymentHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments", null=True)
    provider = models.CharField(max_length=50)  # razorpay/stripe
    provider_order_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)  # succeeded/failed/pending
    raw_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
