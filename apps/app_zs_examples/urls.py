from django.conf.urls import url
from apps.app_zs_examples import views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

app_name = 'app_zs_examples'

router = routers.DefaultRouter()

api_urlpatterns_swagger = [
	url(r'^rest_api/v3/orm/get/test_table_model/$', views.test_table_model__RestApi__View.as_view(), name="test_table_model_list"),
    url(r'^rest_api/v3/orm/get/test_table_model/(?P<id>[0-9]+)/$', views.test_table_model__RestApi__View.as_view(), name="test_table_model_get"),
	url(r'^rest_api/v3/orm/create/test_table_model/', views.test_table_model__RestApi__Create.as_view(), name="test_table_model_create"),
	url(r'^rest_api/v3/orm/update/test_table_model/(?P<id>[0-9]+)/$', views.test_table_model__RestApi__Update.as_view(), name="test_table_model_update"),
	url(r'^rest_api/v3/orm/delete/test_table_model/(?P<id>[0-9]+)/$', views.test_table_model__RestApi__Delete.as_view(), name="test_table_model_delete"),
]

schema_view = get_schema_view(
   openapi.Info(
      title="DjangoAnalytics API",
      default_version='v1',
      description="Dynamic ORM Api",
      terms_of_service="https://djangoanalytics.com/policies/terms/",
      contact=openapi.Contact(email="admin@djangoanalytics.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   patterns=api_urlpatterns_swagger,
   #permission_classes=(permissions.AllowAny,),
)

api_urlpatterns = [
	url(r'^rest_api/', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

	url(r'^rest_api/v3/orm/get/test_table_model/$', views.test_table_model__RestApi__View.as_view(), name="test_table_model_list"),
    url(r'^rest_api/v3/orm/get/test_table_model/(?P<id>[0-9]+)/$', views.test_table_model__RestApi__View.as_view(), name="test_table_model_get"),
    url(r'^rest_api/v3/orm/get/test_table_model/export/(?P<document_type>\w+)/$', views.test_table_model__RestApi__export.as_view(), name="export_files"),
    url(r'^rest_api/v3/orm/get/test_table_model/(?P<id>[0-9]+)/export/(?P<document_type>\w+)/$', views.test_table_model__RestApi__export.as_view(), name="export_files"),
    url(r'^rest_api/v3/orm/get/test_table_model/import/$', views.test_table_model__RestApi__import.as_view(), name="import_files"),
	url(r'^rest_api/v3/orm/create/test_table_model/', views.test_table_model__RestApi__Create.as_view(), name="test_table_model_create"),
	url(r'^rest_api/v3/orm/update/test_table_model/(?P<id>[0-9]+)/$', views.test_table_model__RestApi__Update.as_view(), name="test_table_model_update"),
	url(r'^rest_api/v3/orm/delete/test_table_model/(?P<id>[0-9]+)/$', views.test_table_model__RestApi__Delete.as_view(), name="test_table_model_delete"),

	url(r'^rest_api/v3/dynamic_orm/get/(?P<request_orm_model>\w+)/$', views.genericTable__RestApi__View.as_view(), name="dynamic_orm_model_get"),
	url(r'^rest_api/v3/dynamic_orm/get/(?P<request_orm_model>\w+)/(?P<id>[0-9]+)/$', views.genericTable__RestApi__View.as_view(), name="dynamic_orm_model_get"),
	url(r'^rest_api/v3/dynamic_orm/get/(?P<request_orm_model>\w+)/export/(?P<document_type>\w+)/$', views.genericTable__RestApi__export.as_view(), name="dynamic_orm_export_files"),
	url(r'^rest_api/v3/dynamic_orm/get/(?P<request_orm_model>\w+)/(?P<id>[0-9]+)/export/(?P<document_type>\w+)/$', views.genericTable__RestApi__export.as_view(), name="dynamic_orm_export_files"),
	url(r'^rest_api/v3/dynamic_orm/get/(?P<request_orm_model>\w+)/import/$', views.genericTable__RestApi__import.as_view(), name="dynamic_orm_import_files"),
	url(r'^rest_api/v3/dynamic_orm/create/(?P<request_orm_model>\w+)/$', views.genericTable__RestApi__Create.as_view(), name="dynamic_orm_model_create"),
	url(r'^rest_api/v3/dynamic_orm/update/(?P<request_orm_model>\w+)/(?P<id>[0-9]+)/$', views.genericTable__RestApi__Update.as_view(), name="dynamic_orm_model_update"),
	url(r'^rest_api/v3/dynamic_orm/delete/(?P<request_orm_model>\w+)/(?P<id>[0-9]+)/$', views.genericTable__RestApi__Delete.as_view(), name="dynamic_orm_model_delete"),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^test_upload_to_model/$', views.test_upload_to_model, name='test_upload_to_model'),
	url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += api_urlpatterns
