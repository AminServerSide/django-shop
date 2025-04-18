from datetime import timezone
from decimal import Decimal

from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    address = models.TextField(blank=True , null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.fullname}" if self.user else f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="item")
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Item of Order #{self.order.id} - {self.product.title}" if self.order and self.product else "Order Item"


class DiscountCode(models.Model):
    name = models.CharField(max_length=15, unique=True)
    discount = models.PositiveSmallIntegerField(default=0)  # stored as a percentage: 10, 25, etc.
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.discount}%"
