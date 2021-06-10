from django.conf.urls import url
from apps.app_opensource_dashboards import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'app_opensource_dashboards'

urlpatterns = [
    url(r'^$', views.index, name='index_app_opensource_dashboards'),
]
