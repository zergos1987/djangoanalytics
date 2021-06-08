from django.conf.urls import url
from apps.database_sqlite_test import views
from django.views.generic import TemplateView
from django.urls import path


urlpatterns = [
    url(r'^$', views.index, name='index_database_sqlite_test'),
]
