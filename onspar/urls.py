"""onspar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from shop.views import product_list
from django.contrib.auth import views as auth_views
from portfolio.views import register

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'', include('portfolio.urls', namespace='portfolio')),
                  url(r'^cart/', include('cart.urls', namespace='cart')),
                  url(r'^shopping/', include('shop.urls', namespace='shop')),
                  # url(r'^', include ('shop.urls', namespace='shop')), #added
                  # url(r'^product/$', views.product_list, name='product_list'),
                  url(r'^login/$', auth_views.login, {'template_name': 'portfolio/login.html'}, name='login'),
                  url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
                  url(r'^auth/', include('social_django.urls', namespace='social')),
                  url(r'^blog/', include('blog.urls', namespace='blog')),
                  url(r'^register/$', auth_views.login, {'template_name': 'account/register.html'}, name='register'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
