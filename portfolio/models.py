from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4
from shop.models import Product

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    bdate = models.DateField(blank=True, null=True)
    photo = models.CharField(max_length=200, db_index=True)
    phoneNumber = models.IntegerField(default=1234567890)
    address = models.CharField(max_length=250,null=True)
    city = models.CharField(max_length=250,null=True)
    country = models.CharField(max_length=250, null=True)
    zipcode = models.IntegerField(default=12345)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)



class Order(models.Model):
    order_id = str(uuid4()).replace('-', '')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    paid = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
