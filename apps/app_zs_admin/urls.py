from django.conf.urls import url
from apps.app_zs_admin import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'app_zs_admin'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
