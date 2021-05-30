from django.conf.urls import url
from apps.accounts import views
from django.urls import path



urlpatterns = [
    url(r'^$', views.index, name='index_accounts'),
]