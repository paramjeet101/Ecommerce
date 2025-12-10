from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def mark_as_paid(self):
        self.is_paid = True
        self.save()

    @classmethod
    def get_unpaid_cart(cls, user):
        cart = cls.objects.filter(user=user, is_paid=False).order_by("-id").first()
        if not cart:
            cart = cls.objects.create(user=user, is_paid=False)
        return cart

    def __str__(self):
        return f"Cart for {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"