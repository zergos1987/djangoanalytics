from django.conf.urls import url
from apps.accounts import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^activation_email_confirm/$', views.activation_email_confirm, name='activation_email_confirm'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
