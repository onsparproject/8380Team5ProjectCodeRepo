from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from shop.views import * #added


now = timezone.now()
def home(request):
    return render(request, 'portfolio/home.html',
                 {'portfolio': home})


