from django.conf.urls import url
from apps.app_zs_admin import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'zs_admin'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^zs_admin/$', views.settings_index, name='settings_index'),
    url(r'^zs_admin/render_view/(?P<id>[0-9]+)/$', views.render_view, name="render_view"),
    url(r'^zs_admin/users_profile/$', views.users_profile, name='users_profile'),
    url(r'^zs_admin/users_profile/create/(?P<username>[\w\-]+)/$', views.users_profile, name='users_profile'),
    url(r'^zs_admin/dashboard_settings/$', views.dashboard_settings, name='dashboard_settings'),
    url(r'^zs_admin/dashboard_creation/$', views.dashboard_creation, name='dashboard_creation'),
    url(r'^zs_admin/dashboard_publication/$', views.dashboard_publication, name='dashboard_publication'),
    url(r'^zs_admin/notification_events_confirm/(?P<user_id>\d+)/$', views.notification_events_confirm, name='notification_events_confirm'),
]
