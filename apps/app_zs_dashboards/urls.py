from django.conf.urls import url
from apps.app_zs_dashboards import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'zs_dashboards'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^render_view/(?P<id>[0-9]+)/$', views.render_view, name="render_view"),
]
