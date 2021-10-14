from django.conf.urls import url
from apps.app_opensource_dashboards import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'os_dashboards'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mb/(?P<id>[0-9]+)/$', views.mb, name='mb'),
]
