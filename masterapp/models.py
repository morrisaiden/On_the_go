from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    COLORS = [
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Purple', 'Purple'),
        ('Pink', 'Pink'),
        ('Black', 'Black'),
        ('White', 'White'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    color = models.CharField(max_length=50, choices=COLORS, default='Black')

    def __str__(self):
        return self.name


class Footwear(models.Model):
    COLORS = [
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Yellow', 'Yellow'),
        ('Purple', 'Purple'),
        ('Pink', 'Pink'),
        ('Black', 'Black'),
        ('White', 'White'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='footwears/')
    color = models.CharField(max_length=50, choices=COLORS, default='Black')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    footwear = models.ForeignKey(Footwear, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        :return: a readable string representation of the cart item
        """
        if self.product:
            return f'{self.quantity} x {self.product.name}'
        elif self.footwear:
            return f'{self.quantity} x {self.footwear.name}'
        else:
            return 'Invalid Cart Item'

    def save(self, *args, **kwargs):
        """
        override save method to ensure price is set correctly based on the item type
        """
        if self.product:
            self.price = self.product.price * self.quantity
        elif self.footwear:
            self.price = self.footwear.price * self.quantity
        super().save(*args, **kwargs)
