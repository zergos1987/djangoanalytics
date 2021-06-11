from django.conf.urls import url
from apps.database_oracle_sadko import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'database_oracle_sadko'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
