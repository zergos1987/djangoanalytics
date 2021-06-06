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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.app_zs_admin.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('os_dashboards/', include('apps.app_opensource_dashboards.urls')),
    path('os_surveys/', include('apps.app_opensource_surveys.urls')),
    path('zs_dashboards/', include('apps.app_zs_dashboards.urls')),
    path('zs_examples/', include('apps.app_zs_examples.urls')),
    path('db_sadko/', include('apps.database_oracle_sadko.urls')),
    path('db_sqlite_test/', include('apps.database_sqlite_test.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)