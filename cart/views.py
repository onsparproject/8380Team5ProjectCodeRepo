from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from portfolio.models import Profile
from .cart import Cart
from .forms import CartAddProductForm, CouponForm
from django.contrib.auth.decorators import login_required



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


def checkout(request):
    my_profile = Profile.objects.all().filter(user=request.user)
    coupon_form = CouponForm()
    cart = Cart(request)
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupons = request.POST["coupons"]
            print("Hey:",coupons)
            for item in cart:
                item['update_quantity_form'] = CartAddProductForm(
                                  initial={'quantity': item['quantity'],'update': True})
                item['quantity_x'] = item['quantity']
            return render(request, 'cart/checkout.html', {'profile': my_profile[0],
                                                            'cart': cart,
                                                            'applied_coupon':coupons,
                                                            'applied':-1})
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                          initial={'quantity': item['quantity'],'update': True})
        item['quantity_x'] = item['quantity']
    return render(request, 'cart/checkout.html', {'profile': my_profile[0],
                                                    'cart': cart,
                                                    'form':coupon_form,
                                                    'applied':10})
