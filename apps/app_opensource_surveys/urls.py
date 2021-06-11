from django.conf.urls import url
from apps.app_opensource_surveys import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'app_opensource_surveys'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
