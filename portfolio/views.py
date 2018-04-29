from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import   UserEditForm, ProfileEditForm, UserRegistrationForm, activationForm, LoginForm
from django.db.models import Sum
from shop.views import * #added
from shop.models import Product
from cart.cart import Cart
from shop.forms import ProductForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from geopy import Nominatim
from django.core.mail import send_mail
from django.http import HttpResponse

now = timezone.now()
def home(request):
    return render(request, 'portfolio/home.html',
                 {'portfolio': home})


def sendConfimationEmail(request):
    profile = Profile.objects.all().filter(user=request.user)[0]
    send_mail('Registration Successful @ Onspar', 'Hello, Thank you for registering with Onspar.\n\n\n Please confirm activation using the token:'+profile.activation_token, 'no-reply@onspar.com', [request.user.email,])
    return  render(request, 'portfolio/emailSent.html')

def activation(request):
    if request.method == 'POST':
        form =  activationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            profile = Profile.objects.all().filter(user=request.user)[0]
            entered_token = cd['entered_token']
            if entered_token == profile.activation_token:
                Profile.objects.all().filter(user=request.user).update(activated=True)
                if profile.profileFilled:
                    return render(request, 'portfolio/home.html')
                else:
                    return redirect('portfolio:fillProfile')
            else:
                form =  activationForm()
                return render(request, 'portfolio/activationPage.html', {'form': form})
    else:
        form =  activationForm()
        return render(request, 'portfolio/activationPage.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form =  LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = authenticate(username=cd['username'],password=cd['password'])
            if new_user is not None:
                if new_user.is_active:
                    login(request, new_user)
                    profile = Profile.objects.all().filter(user=request.user)[0]
                    if profile.activated:
                        if profile.profileFilled:
                            return redirect('portfolio:home')
                        else:
                            return redirect('portfolio:fillProfile')
                    else:
                        return redirect('portfolio:activation')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'portfolio/login.html', {'form':form})



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
            profile = Profile.objects.create(user=new_user)
            send_mail('Registration Successful @ Onspar', 'Hello, Thank you for registering with Onspar. Please confirm activation using the token:'+profile.activation_token, 'no-reply@onspar.com', [new_user.email,])
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

def notifications(request):
    products = Product.objects.all()
    requireRestock = []
    for product in products:
        if (product.stock <= 20):
            requireRestock.append(product)
    return render(request,'portfolio/notifications.html',{'notifications': requireRestock})


@login_required
def myProfile(request):
    my_profile = Profile.objects.all().filter(user=request.user)
    if len(my_profile) > 0 and my_profile[0].profileFilled:
        geolocator = Nominatim()
        location = geolocator.geocode(str(my_profile[0].address)+", "+str(my_profile[0].city))
        return render(request,
                      'portfolio/myProfile.html',
                      {'user': request.user,
                      'profile': my_profile[0],
                      'lat': location.latitude,
                      'long': location.longitude,
                      'loc': str(my_profile[0].address)+", "+str(my_profile[0].city)})

    else:
        my_profile = Profile.objects.all().filter(user=request.user)
        if len(my_profile) == 0:
            profile = Profile.objects.create(user=request.user)
        return redirect('portfolio:fillProfile')


@login_required
def fillProfile(request):
    if request.method == 'POST':
        profile = Profile.objects.all().filter(user=request.user)[0]
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                       data=request.POST,
                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            Profile.objects.all().filter(user=request.user).update(profileFilled=True)
            return redirect('portfolio:home')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
        instance=request.user.profile)
        return render(request,
                  'portfolio/fillProfile.html',
                  {'user_form': user_form,

                  'profile_form': profile_form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                       data=request.POST,
                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
        instance=request.user.profile)
    return render(request,
                  'portfolio/editProfile.html',
                  {'user_form': user_form,
                  'profile_form': profile_form})




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
