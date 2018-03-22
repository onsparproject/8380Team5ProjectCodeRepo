
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_descr = models.CharField(max_length=250,default='null')
    product_id = models.IntegerField(blank=False, null=False)
    product_type = models.CharField(max_length=50)
    product_cost = models.IntegerField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.client_number)


#class Blog(models.Model):
 #   name = models.CharField(max_length=50)
  #  item_number = models.IntegerField(blank=False, null=False)
   # item_type = models.CharField(max_length=50)
    #description = models.CharField(max_length=200)
   # qty_on_hand = models.IntegerField(blank=False, null=False)
   # expired_date = models.DateTimeField(default=timezone.now)
   # created_date = models.DateTimeField(default=timezone.now)
   # updated_date = models.DateTimeField(auto_now_add=True)

    #def created(self):
     #   self.created_date = timezone.now()
      #  self.save()

   # def updated(self):
    #    self.updated_date = timezone.now()
     #   self.save()

   # def __str__(self):
    #    return str(self.item_number)

