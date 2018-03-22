from django.contrib import admin
from .models import Product

class ProductList(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'product_type', 'product_descr')
    list_filter = ('product_id', 'product_name', 'product_type')
    search_fields = ('product_id', 'product_name')
    ordering = ['product_id']



admin.site.register(Product, ProductList)

