from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
        url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/Eng/$', views.product_detail, name='product_detail'),
        url(r'^(?P<id>\d+)/French/$', views.french, name='French'),
        url(r'^(?P<id>\d+)/Spanish/$', views.spanish, name='Spanish'),
        url(r'^(?P<id>\d+)/Hindi/$', views.hindi, name='Hindi'),
        url(r'^addReview/(?P<id>\d+)/$', views.add_review, name='addReview'),
        #Root url
        url(r'^$', views.product_list, name='product_list'),
        ]
