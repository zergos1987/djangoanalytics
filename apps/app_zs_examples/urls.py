from django.conf.urls import url
from apps.app_zs_examples import views
from django.urls import path



urlpatterns = [
    url(r'^$', views.index, name='index_app_zs_examples'),
]