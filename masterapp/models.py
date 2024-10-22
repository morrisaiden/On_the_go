from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Footwear(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    footwear = models.ForeignKey(Footwear, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f'{self.quantity} x {self.product.name}'
        elif self.footwear:
            return f'{self.quantity} x {self.footwear.name}'
        else:
            return 'Invalid Cart Item'
