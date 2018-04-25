from django.conf.urls import url
from . import views
from shop.views import product_list
from blog.views import post_list
from django.conf.urls.static import static

app_name ='portfolio'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
  #  url(r'^profile/$', views.profile, name='profile'),
    url(r'^employee_view/$', views.employee, name='employee_view'),
  	url(r'^product/$', views.product_list, name='product_list'), #added
    url(r'^product/create/$', views.product_new, name='product_new'),
    url(r'^product/(?P<pk>\d+)/delete/$', views.employee_product_delete, name='product_delete'),
    url(r'^product/(?P<pk>\d+)/edit/$', views.employee_product_edit, name='product_edit'),
  #  url(r'^account_settings_list/$', views.account_settings_list, name='account_settings_list'),
    url(r'^register/$', views.register, name='register'),
   # url(r'^blog/$', views.post_list, name='post_list'),

]
