from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import  UserRegistrationForm
from django.db.models import Sum
from shop.views import * #added
from shop.models import Product
from shop.forms import ProductForm
from django.contrib.auth.decorators import login_required

now = timezone.now()
def home(request):
    return render(request, 'portfolio/home.html',
                 {'portfolio': home})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})
def employee(request):
    products = Product.objects.filter(available=True)
    return render(request, 'portfolio/admin.html', {'products': products})

@login_required
def employee_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print("I am here")
    if request.method == "POST":
        # update
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated = timezone.now()
            product.save()
            products = Product.objects.filter(available=True)
            return render(request, 'portfolio/admin.html', {'products': products})
    else:
        # edit
        print("I am here")
        form = ProductForm(instance=product)
    return render(request, 'portfolio/product_update.html', {'form': form})


@login_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created = timezone.now()
            product.save()
            products = Product.objects.filter(available=True)
            return render(request, 'portfolio/admin.html',
                          {'products': products})
    else:
        form = ProductForm()
        return render(request, 'portfolio/product_add.html', {'form': form})



@login_required
def employee_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('portfolio:employee_view')
