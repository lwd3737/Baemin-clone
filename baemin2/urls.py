from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^category/(?P<slug>[-\w]+)/$', views.category_detail, name='category_detail'),
	url(r'^category/(?P<category_pk>\d+)/shop/(?P<pk>\d+)/$', views.shop_detail, name='shop_detail'),
	#url(r'^category/(?P<category_pk>\d+)$')
]