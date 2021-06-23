from django.conf.urls import url
from apps.app_zs_admin import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'app_zs_admin'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('403/', TemplateView.as_view(template_name="app_zs_admin/403.html"),name='403'),
    path('404/', TemplateView.as_view(template_name="app_zs_admin/404.html"),name='404'),
]
