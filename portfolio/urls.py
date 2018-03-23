from django.conf.urls import url
from . import views
from shop.views import product_list

app_name ='portfolio'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
  	url(r'^product/$', views.product_list, name='product_list'), #added

]