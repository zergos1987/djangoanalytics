"""djangoanalytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
#initialize_base_content ##########################
if not os.getenv('initialazie_base_content'):
    os.environ['initialazie_base_content'] = str(os.getpid())
    from custom_script_extensions.djangoanalytics_initialize import initialazie_base_content
    initialazie_base_content()
    
    
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from apps.accounts import views as accounts_views

from django.shortcuts import redirect


urlpatterns = [
    url(r'^adminlogout/$', accounts_views.signout, name='signout'),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin', admin.site.urls),
    path('', include('apps.app_zs_admin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('os_dashboards/', include('apps.app_opensource_dashboards.urls')),
    path('os_surveys/', include('apps.app_opensource_surveys.urls')),
    path('zs_dashboards/', include('apps.app_zs_dashboards.urls')),
    path('zs_examples/', include('apps.app_zs_examples.urls')),
    path('db_sadko/', include('apps.database_oracle_sadko.urls')),
    path('db_sqlite_test/', include('apps.database_sqlite_test.urls')),
]

urlpatterns += [
    url(r'^accounts/signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^reset/$', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'), name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(
          template_name='registration/password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(
          template_name='registration/password_change_done.html'),
        name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
