from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
ORDER_STATUS = (
    ("PENDING", "Pending"),
    ("PLACED", "Placed"),
    ("SHIPPED", "Shipped"),
    ("DELIVERED", "Delivered"),
    ("CANCELLED", "Cancelled"),
)


PAYMENT_STATUS = (
    ("PENDING", "Pending"),
    ("PAID", "Paid"),
    ("FAILED", "Failed"),
    ("REFUNDED", "Refunded"),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PENDING")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="PENDING")

    shipping_address = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at purchase time
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"