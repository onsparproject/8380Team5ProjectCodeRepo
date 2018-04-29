from django.contrib import admin
from .models import Profile, OrderItem, Order



class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phoneNumber']

admin.site.register(Profile, ProfileAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'total_price',
                    'paid',
                    'created',
                    'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
