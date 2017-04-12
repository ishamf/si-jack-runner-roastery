from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout),
    url(r'^p/(?P<pk>[0-9]+)/$', views.ProductView.as_view(), name='detail'),
    url(r'^c/$', views.cart_view, name='cart'),
    url(r'^c/add/(?P<pk>[0-9]+)/$', views.add_cart, name='add_cart'),
    url(r'^c/remove/(?P<pk>[0-9]+)/$', views.remove_cart, name='remove_cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.order, name='order'),
    url(r'^orders/(?P<pk>[0-9]+)/resolve/$', views.resolve_order, name='resolve_order'),
    url(r'^statistics/$', views.statistics, name='orders'),
]
