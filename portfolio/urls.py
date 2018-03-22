from django.conf.urls import url
from . import views

app_name ='portfolio'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
   # url(r'^client/$', views.product_list, name='product_list'),

]