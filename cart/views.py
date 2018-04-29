from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from shop.models import Product
from decimal import Decimal
from django.core.urlresolvers import reverse
from portfolio.models import Profile, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm, CouponForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from paypal.standard.forms import  PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt



@require_POST
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                          initial={'quantity': item['quantity'],'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


def payment(request):
    cart = Cart(request)
    confirmed_order = Order(total_price=priceCalculator(cart))
    confirmed_order.save()
    target_order = get_object_or_404(Order, id=confirmed_order.id)
    count = 0
    for item in cart:
        count = count + 1
        if item['product'].price != '' and item['quantity'] != '':
            OrderItem(order=confirmed_order, product=item['product'], price=item['product'].price, quantity=item['quantity']).save()
    print("The confirmed order ID is:", confirmed_order.id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': priceCalculator(cart).quantize(Decimal('.01')),
        'item_name': 'Order{}'.format(confirmed_order.id),
        'invoice': str(confirmed_order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('cart:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('cart:canceled')),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,
                  'cart/process.html',
                  {'order': target_order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'cart/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'cart/canceled.html')


def priceCalculator(cart):
    total_price = 0
    for item in cart:
        total_price = total_price + item['quantity'] * item['product'].price
    tax = (total_price / 100) * 7
    shipping = (total_price / 100) * 2
    total_price = total_price + tax + shipping
    return total_price


def checkout(request):
    my_profile = Profile.objects.all().filter(user=request.user)
    coupon_form = CouponForm()
    cart = Cart(request)
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupons = request.POST["coupons"]
            for item in cart:
                item['update_quantity_form'] = CartAddProductForm(
                                  initial={'quantity': item['quantity'],'update': True})
            return render(request, 'cart/checkout.html', {'profile': my_profile[0],
                                                            'cart': cart,
                                                            'applied_coupon':coupons,
                                                            'applied':-1,
                                                           'server_price':priceCalculator(cart)})
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                          initial={'quantity': item['quantity'],'update': True})
    return render(request, 'cart/checkout.html', {'profile': my_profile[0],
                                                    'cart': cart,
                                                    'form':coupon_form,
                                                    'applied':10,
                                                  'server_price': priceCalculator(cart)})
