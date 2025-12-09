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


    @classmethod
    def get_or_create_cart_from_items(cls, user, cart_items):
        cart = cls.objects.filter(user=user, is_paid=False).order_by("-id").first()
        if not cart:
            cart = cls.objects.create(user=user, is_paid=False)

        valid_competition_ids = []

        for item in cart_items:
            comp = Competition.objects.filter(id=item.get("competition_id")).first()
            if not comp:
                continue

            spins = int(item.get("spins", 0))
            if spins <= 0:
                continue

            CartItem.objects.update_or_create(
                cart=cart,
                competition=comp,
                defaults={"spins": spins}
            )
            valid_competition_ids.append(comp.id)


        cart.items.exclude(competition_id__in=valid_competition_ids).delete()

        return cart


    def __str__(self):
        return f"Cart for {self.user.email}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"