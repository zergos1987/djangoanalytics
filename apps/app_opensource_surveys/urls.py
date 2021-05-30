from django.conf.urls import url
from apps.app_opensource_surveys import views
from django.urls import path



urlpatterns = [
    url(r'^$', views.index, name='index_app_opensource_surveys'),
]