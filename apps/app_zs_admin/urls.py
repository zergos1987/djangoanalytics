from django.conf.urls import include, url
from apps.app_zs_admin import views
from django.views.generic import TemplateView
from django.urls import path

app_name = 'zs_admin'
router = views.api_root()

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^zs_admin/$', views.settings_index, name='settings_index'),
    url(r'^zs_admin/render_view/(?P<id>[0-9]+)/$', views.render_view, name="render_view"),
    url(r'^zs_admin/users_profile/$', views.users_profile, name='users_profile'),
    url(r'^zs_admin/users_profile/create/(?P<username>[\w\-]+)/$', views.users_profile, name='users_profile'),
    url(r'^zs_admin/notification_events_publication/$', views.notification_events_publication, name='notification_events_publication'),
    url(r'^zs_admin/notification_events_publication/(?P<event>[\w\-]+)/$', views.notification_events_publication, name='notification_events_publication'),
    url(r'^zs_admin/notification_events_publication/(?P<notification_events_id>[0-9]+)/(?P<event>[\w\-]+)/$', views.notification_events_publication, name='notification_events_publication'),
    url(r'^zs_admin/dashboard_settings/$', views.dashboard_settings, name='dashboard_settings'),
    url(r'^zs_admin/dashboard_creation/$', views.dashboard_creation, name='dashboard_creation'),
    url(r'^zs_admin/dashboard_publication/$', views.dashboard_publication, name='dashboard_publication'),
    url(r'^zs_admin/notification_events_confirm/(?P<user_id>\d+)/$', views.notification_events_confirm, name='notification_events_confirm'),
    url(r'^zs_admin/get_user_message/$', views.get_user_message, name='get_user_message'),
    
    url(r'^zs_admin/api/', include(router.urls)),
    url(r'^zs_admin/api/(?P<api_key>\w+)/etl_scheduller/get/$', views.etl_scheduller_get_api.as_view(), name="etl_scheduller_get_api"),
    url(r'^zs_admin/api/(?P<api_key>\w+)/etl_scheduller/get/(?P<id>[0-9]+)/$', views.etl_scheduller_get_api.as_view(), name="etl_scheduller_get_api"),
    url(r'^zs_admin/api/(?P<api_key>\w+)/etl_scheduller/update/(?P<id>[0-9]+)/$', views.etl_scheduller_update_api.as_view(), name="etl_scheduller_update_api"),
]
