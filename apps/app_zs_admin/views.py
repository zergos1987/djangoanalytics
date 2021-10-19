from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse
 
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType 
from apps.accounts.models import user_extra_details
from apps.app_zs_admin.models import app, notification_events, user_notification_event_confirm, aside_left_menu_includes, etl_job_database_tables_tasks, etl_job_database_tables_tasks_logs
from custom_script_extensions.dynamic_grid_tables import get_table_settings
from custom_script_extensions.dynamic_grid_render import dynamic_datagrid
from custom_script_extensions.custom_permissions_check import check_user_content_request_permission
from custom_script_extensions.forms import UserZsAdminForm, ContentpublicationsForm, notificationCreationForm

from django.core.serializers import serialize
from django.http.response import JsonResponse
import json

import random, string
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import FloatField, CharField
from django.db.models.functions import Cast
from django.db.models import Max, Case, Value, When
from django.db.models import Aggregate, CharField, Value
import re

import os
from decouple import config


import django_filters.rest_framework
from rest_framework.parsers import FileUploadParser
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied as DRF_PermissionDenied
from rest_framework import routers
from django.utils.safestring import mark_safe

from custom_script_extensions.drf_serializers import (etl_job_database_tables_tasks__Serializer, etl_job_database_tables_tasks__update_create_Serializer)


# Create your views here.
#@method_decorator([login_required, permission_required("app_zs_admin.view_app")], name="dispatch")
@login_required
#@permission_required('app_zs_admin.view_app')
def index(request):
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]


	if 'zs_admin' != app_settings.app_start_page:
		return HttpResponseRedirect(f'/{app_settings.app_start_page}/')
	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
	}

	template = 'app_zs_admin/index.html' 

	return render(request, template, context)


@login_required
@permission_required('app_zs_admin.view_app')
def settings_index(request):
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
	}

	template = 'app_zs_admin/app_settings.html' 

	return render(request, template, context)


@login_required
#@permission_required('app_zs_admin.view_app')
def render_view(request, id):
	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=id,
		user_id=request.user.id) 

	if not user_content_has_permission: raise PermissionDenied()

	user_content_selected = aside_left_menu_includes.objects.get(id=id)
	content_source_type = user_content_selected.source_type

	application_settings = {}
	if content_source_type == 'internal':
		print('internal', user_content_selected.source_app_name, user_content_selected.href, user_content_selected.id)
		try:
			return redirect(reverse(f"{user_content_selected.source_app_name}:{user_content_selected.href}"))
		except Exception as e:
			print(str(e))
		#return redirect('{}?flag=True&user_id=23'.format(reverse(f"{user_content_selected.render_app_name}:{user_content_selected.href}")))
	if content_source_type == 'external' and 'http' not in user_content_selected.external_href:
		print('external', user_content_selected.source_app_name, user_content_selected.href, user_content_selected.id)
		try:
			return redirect(reverse(f"{user_content_selected.source_app_name}:{user_content_selected.href}", kwargs={'id': user_content_selected.id}))
		except Exception as e:
			print(str(e))

	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	template = 'app_zs_admin/render_view.html'
	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
		'app_view_object': {},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}
	return render(request, template, context)


@login_required
#@permission_required('app_zs_admin.view_app')
def handler400(request, exception):
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/400.html", context)
	response.status_code = 400
	return response


@login_required
#@permission_required('app_zs_admin.view_app')
def handler403(request, exception):
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/403.html", context)
	response.status_code = 403
	return response


@login_required
#@permission_required('app_zs_admin.view_app')
def handler404(request, exception):
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/404.html", context)
	response.status_code = 404
	return response


@login_required
#@permission_required('app_zs_admin.view_app')
def handler500(request):
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/500.html", context)
	response.status_code = 500
	return response


# internal views ################################################################
@login_required
#@permission_required('app_zs_admin.view_app')
def notification_events_confirm(request, user_id):
	u = User.objects.get(id=user_id)
	if u:
		obj, created = user_notification_event_confirm.objects.update_or_create(
			user=u
		)
		if not created:
			events = user_notification_event_confirm.objects.filter(user=u).first()
			events.save()
	else:
		return HttpResponse(500)
	return HttpResponse(200)


@login_required
#@permission_required('app_zs_admin.view_app')
def notification_events_publication(request, notification_events_id=None, event=None):
	if notification_events_id and event:
		if request.method == 'POST':
			if event == 'edit_row':
				form = notificationCreationForm(request.POST, id=notification_events_id)
				if form.is_valid():
					form.save(commit=False)
					obj = notification_events.objects.filter(id=notification_events_id).all()
					return HttpResponse(serialize("json", obj), content_type='application/json', status = 200)
			if event == 'delete_row':
				notification_events.objects.filter(id=notification_events_id).delete()
		return HttpResponse(200)


	user_content_selected = aside_left_menu_includes.objects.filter(href='notification_events_publication', is_actual=True).first()

	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=user_content_selected.id,
		user_id=request.user.id)
	if not user_content_has_permission: raise PermissionDenied()

	form_detail_list = {'id': 'detail_notificationCreationForm', 'data': ''}
	#form_detail_list['data'] = serialize("json", notification_events.objects.all()) #.filter(is_actual=True)
	form_detail_list['data'] = notification_events.objects.all() #.filter(is_actual=True)
	
	if request.method == 'POST':
		form = notificationCreationForm(request.POST, id=None)
		if form.is_valid():
			form.save(commit=False)
			return HttpResponse(200)
			#return HttpResponseRedirect(request.path_info)
	else:
		form = notificationCreationForm()


	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
		'app_view_object': {'object': form, 'object_type': 'form', 'form_detail_list': form_detail_list},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)


@login_required
#@permission_required('app_zs_admin.view_app')
def users_profile(request, username=None):
	user_content_selected = aside_left_menu_includes.objects.filter(href='users_profile', is_actual=True).first()

	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=user_content_selected.id,
		user_id=request.user.id)
	if not user_content_has_permission: raise PermissionDenied()

	if username is not None:
		if len(username) > 3:
			print('creating new user', username, request.path_info)
			u, created = User.objects.get_or_create(username=username)
			request_path = f'/zs_admin/users_profile/'
			if created:
				u.is_active = False
				u.save()
				user_extra_details.objects.filter(user=u).update(ldap_is_active=True)
				request_path = request_path + f'?user_id={u.id}'
			return HttpResponseRedirect(request_path)

	if request.method == 'POST':
		form = UserZsAdminForm(request.POST, request.GET)
		if form.is_valid():
			form.save(commit=False)
			args = form.cleaned_data.get('the_user', '-')
			request_path = request.path_info + '?user_id=' + args
			return HttpResponseRedirect(request_path)
	else:
		form = UserZsAdminForm(request.GET)


	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]

	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
		'app_view_object': {'object': form, 'object_type': 'form'},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)



@login_required
#@permission_required('app_zs_admin.view_app')
def dashboard_settings(request):
	user_content_selected = aside_left_menu_includes.objects.filter(href='dashboard_settings', is_actual=True).first()

	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=user_content_selected.id,
		user_id=request.user.id)
	if not user_content_has_permission: raise PermissionDenied()


	datagrid_request = request.GET.get("request_type", request.POST.get("request_type", None))
	request_table = request.GET.get("request_table", request.POST.get("request_table", None))
	tables_list = ['aside_left_menu_includes', 'user_extra_details', 'group']
	object_list = []
	for t in tables_list:
		table_settings = get_table_settings(table_name=t, url_for_render='/zs_admin/dashboard_settings/', request=request)
		if datagrid_request == 'datagrid' and t == request_table :
			#processing
			data = dynamic_datagrid(
				fathgrid_initialize_settings=None,
				request=request,
				request_table=request_table,
				request_table_columns_id=table_settings.get('request_table_columns_id'),
				request_table_columns_props=table_settings.get('request_table_columns_props'),
				request_table_filters=table_settings.get('request_table_filters'),
				request_table_excludes=table_settings.get('request_table_excludes'),
				request_table_secure_values_hide=table_settings.get('request_table_secure_values_hide'),
				request_table_max_limit_rows=table_settings.get('request_table_max_limit_rows'),
				add_row_default=table_settings.get('add_row_default')), 
			if data == 500 or data == 'dynamic grid error': return HttpResponse(status=500)
			return data[0]
		else:
			#initialize
			object_list.append({
				'object': dynamic_datagrid(
					fathgrid_initialize_settings=table_settings.get('fathgrid_initialize_settings'), 
					request=request, 
					request_table=table_settings.get('table_name'), 
					request_table_title=table_settings.get('request_table_title'),
					request_table_as_dict=table_settings.get('request_table_as_dict'),
					request_table_columns_id=table_settings.get('request_table_columns_id'),
					request_table_columns_props=table_settings.get('request_table_columns_props'),
					request_m2m_join_columns=table_settings.get('request_m2m_join_columns'),
					textarea_select_options=table_settings.get('textarea_select_options'),
					add_row_default=table_settings.get('add_row_default'),
					get_media=table_settings.get('get_media')), 
				'object_type': 'dynamic_datagrid'
			})

	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]
	
	template = 'app_zs_admin/render_view.html'
	
	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
		'app_view_object': object_list,
		'app_view_object_settings': user_content_selected, 
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)



@login_required
def dashboard_creation(request):
	user_content_selected = aside_left_menu_includes.objects.filter(href='dashboard_creation', is_actual=True).first()

	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=user_content_selected.id,
		user_id=request.user.id)
	if not user_content_has_permission: raise PermissionDenied()

	OS_DASHBOARDS_METABASE_URL = os.environ.get("OS_DASHBOARDS_METABASE_URL", config('OS_DASHBOARDS_METABASE_URL'))
	OS_DASHBOARDS_METABASE_SECRET_KEY = os.environ.get("OS_DASHBOARDS_METABASE_SECRET_KEY", config('OS_DASHBOARDS_METABASE_SECRET_KEY'))
	OS_DASHBOARDS_METABASE_LOGIN = os.environ.get("OS_DASHBOARDS_METABASE_LOGIN", config('OS_DASHBOARDS_METABASE_LOGIN'))
	OS_DASHBOARDS_METABASE_PSW = os.environ.get("OS_DASHBOARDS_METABASE_PSW", config('OS_DASHBOARDS_METABASE_PSW'))
	
	return redirect(OS_DASHBOARDS_METABASE_URL)#HttpResponse(200)



@login_required
def dashboard_publication(request):
	user_content_selected = aside_left_menu_includes.objects.filter(href='dashboard_publication', is_actual=True).first()

	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=user_content_selected.id,
		user_id=request.user.id)
	if not user_content_has_permission: raise PermissionDenied()


	if request.method == 'POST':
		form = ContentpublicationsForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			return HttpResponseRedirect(request.path_info)
	else:
		form = ContentpublicationsForm()


	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(Q(is_actual=True) & Q(event_date__gte=confirm_events_user.confirm_date) & Q(Q(users_list=request.user) | Q(title='Новый пользователь!'))).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]
	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
		'app_view_object': {'object': form, 'object_type': 'form'},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)



# ETL api #####################################
class MyAPIRootView(routers.APIRootView):
	"""
	Controls appearance of the API root view
	"""
	def get_view_name(self) -> str:
		return "DjangoAnalytics API v1.0.0"

	def get_view_description(self, html=False) -> str:
		header = "Api urls page"
		body = """<ul>
			<li><small><strong>ETL Scheduller [GET]</strong>:   /zs_admin/api/<strong style="color: blue;">API_KEY</strong>/etl_scheduller/get/</small></li>
			<li><small><strong>ETL Scheduller [GET]</strong>:   /zs_admin/api/<strong style="color: blue;">API_KEY</strong>/etl_scheduller/get/<strong style="color: blue;">id</strong>/</small></li>
			<li><small><strong>ETL Scheduller [POST]</strong>:   /zs_admin/api/<strong style="color: blue;">API_KEY</strong>/etl_scheduller/update/<strong style="color: blue;">id</strong>/</small></li>
		</ul>"""
		if html:
			return mark_safe(f"</br><div><strong>{header}:</strong></div></br><div>{body}</div></br>")
		else:
			return header

class api_root(routers.DefaultRouter):
	APIRootView = MyAPIRootView

class Searchpagination__1__(PageNumberPagination):
	page_size = 1
	page_size_query_param = 'p'
	max_page_size = 100

def GetFilterType(field, fieldType):
	if fieldType == 'AutoField':
		filter_type = ['exact', 'range']
	elif fieldType == 'CharField':
		filter_type = ['icontains']
	elif fieldType == 'DateTimeField':
		filter_type = ['year__gt', 'year__lt', 'range']
	elif fieldType == 'DateField':
		filter_type = ['year__gt', 'year__lt', 'range']
	elif fieldType == 'IntegerField':
		filter_type = ['gte', 'lte', 'range']
	elif fieldType == 'BooleanField':
		filter_type = ['exact']
	elif fieldType == 'TextField':
		filter_type = ['icontains']
	elif fieldType == 'ManyToManyField':
		filter_type = ['icontains']
	elif fieldType == 'ForeignKey':
		filter_type = ['icontains']
	else:
		filter_type = None
	return filter_type

class etl_scheduller_APIKeyPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		Access = False
		ETL_API_KEY = os.getenv('ETL_API_KEY_os', config('ETL_API_KEY_env'))
		ETL_REQUEST_API_KEY = request.GET.get('api_key', False)
		if ETL_REQUEST_API_KEY == ETL_API_KEY:
			Access = True
		else:
			URL = request.get_full_path()
			if ETL_API_KEY in URL:
				for i in URL.split('/'):
					if i == ETL_API_KEY:
						Access = True
		return Access

class etl_scheduller_get_api(generics.ListAPIView):
	permission_classes = [etl_scheduller_APIKeyPermission]
	filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
	filterset_fields = {}
	#pagination_class = Searchpagination__1__
	search_fields = []
	ordering_fields = 'id'#'__all__'
	ordering = ['id']

	lookup_field = 'id'    
	lookup_url_kwarg = 'id'


	def options(self, request, *args, **kwargs):
		meta = self.metadata_class()
		data = meta.determine_metadata(request, self)

		table_name = etl_job_database_tables_tasks.__name__

		for key in data:
			if key == 'name':
				data[key] = 'DjangoAnalytics Api. v.1.0.0'
			elif key == 'description':
				data[key] = f'Get list or by id. Table name: {table_name}. --- Example #1: /zs_admin/api/api_key/etl_scheduller/get/ --- Example #2: /zs_admin/api/api_key/etl_scheduller/get/id/'

		return Response(data=data, status=status.HTTP_200_OK)

	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	def get_queryset(self):
		try:
			model = etl_job_database_tables_tasks
			related_fields = ['update_week_days_list__update_week_days_list', 'update_time_list__update_time_list', 'created_by__username', 'updated_by__username']
			column_names = [f.name for f in model._meta.get_fields() if GetFilterType(f, f.get_internal_type()) != None and not f.name.startswith('for_')]
			column_names_new = []
			for c in column_names:
				related_c = [r for r in related_fields if c == r[:r.index('__')]]
				if len(related_c) > 0: 
					related_c = related_c[0]
					c = related_c
				column_names_new.append(c)
			etl_scheduller_get_api.search_fields = column_names_new
			filterset_fields_temp = {}
			for field in model._meta.get_fields():
				field_name = field.name
				filter_type = GetFilterType(field, field.get_internal_type())
				if filter_type is not None and not field_name.startswith('for_'):
					for r in column_names_new:
						if '__' in r:
							if field_name == r[:r.index('__')]:
								field_name = r
					filterset_fields_temp[field_name] = filter_type
			etl_scheduller_get_api.filterset_fields = filterset_fields_temp
			if self.kwargs.get(self.lookup_url_kwarg):
				_id = self.kwargs.get(self.lookup_url_kwarg)
				queryset = model.objects.filter(id=_id)

			else:
				queryset = model.objects.all()#.order_by('-id')
			return queryset
		except Exception as e:
			print(str(e))
			raise Http404


	def get_serializer_class(self):
		etl_job_database_tables_tasks__Serializer.Meta.model = etl_job_database_tables_tasks
		return etl_job_database_tables_tasks__Serializer


class etl_scheduller_update_api(generics.RetrieveUpdateAPIView):
	permission_classes = [etl_scheduller_APIKeyPermission]
	lookup_field = 'id'
	lookup_url_kwarg = 'id'

	def options(self, request, *args, **kwargs):
		meta = self.metadata_class()
		data = meta.determine_metadata(request, self)

		table_name = etl_job_database_tables_tasks.__name__

		for key in data:
			if key == 'name':
				data[key] = 'DjangoAnalytics Api. v.1.0.0'
			elif key == 'description':
				data[key] = f'Update by id. Get updated. Table name: {table_name}. --- Example #1: /zs_admin/api/api_key/etl_scheduller/update/id/'

		return Response(data=data, status=status.HTTP_200_OK)

	def get_serializer_class(self):
		etl_job_database_tables_tasks__update_create_Serializer.Meta.model = etl_job_database_tables_tasks
		return etl_job_database_tables_tasks__update_create_Serializer

	def get_queryset(self):
		try:
			model = etl_job_database_tables_tasks
			return model.objects.all()
		except Exception as e:
			raise Http404

	def put(self, request, *args, **kwargs):
		_id = self.kwargs.get(self.lookup_url_kwarg)
		model = etl_job_database_tables_tasks
		if len(list(request.data)) > 10:
			serializer = etl_job_database_tables_tasks__update_create_Serializer(model.objects.get(id=_id), data=request.data)
		else:
			serializer = etl_job_database_tables_tasks__update_create_Serializer(model.objects.get(id=_id), data=request.data.get('data'), partial=True)
			
			logs = etl_job_database_tables_tasks_logs(
				etl_job_database_tables_tasks_fk=model.objects.get(id=_id),
				table_rows_count=int(request.data.get('logs').get('rows_count')),
				error_message=request.data.get('logs').get('error_message')
				)
			logs.save()

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
