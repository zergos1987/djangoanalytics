from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse

from django.contrib.auth.models import User, Group, Permission, ContentType
from apps.app_zs_admin.models import app, notification_events, user_notification_event_confirm, aside_left_menu_includes
from custom_script_extensions.custom_permissions_check import check_user_content_request_permission
from custom_script_extensions.forms import UserZsAdminForm, ContentpublicationsForm

import os
from decouple import config


# Create your views here.
#@method_decorator([login_required, permission_required("app_zs_admin.view_app")], name="dispatch")
@login_required
#@permission_required('app_zs_admin.view_app')
def index(request):
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
	if content_source_type == 'external':
		print('external', user_content_selected.source_app_name, user_content_selected.href, user_content_selected.id)
		try:
			return redirect(reverse(f"{user_content_selected.source_app_name}:{user_content_selected.href}", kwargs={'id': user_content_selected.id}))
		except Exception as e:
			print(str(e))

	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
def users_profile(request):
	user_content_selected = aside_left_menu_includes.objects.filter(href='users_profile', is_actual=True).first()

	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=user_content_selected.id,
		user_id=request.user.id)
	if not user_content_has_permission: raise PermissionDenied()


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
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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

	app_view_object = {
		'content_id': 1, 
		'user_id': 1, 
		'content_type': 'form',
		'content': 'form_object'
	}
	app_settings = app.objects.filter(is_actual=True).first()
	confirm_events_user = user_notification_event_confirm.objects.filter(user=request.user).first()
	app_events = {}
	if confirm_events_user:
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
		app_events['previews'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__lte=confirm_events_user.confirm_date).all()[:3]
	else:
		app_events['actual'] = notification_events.objects.filter(is_actual=True).all()[:5]
	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'app_events': app_events,
		'app_settings_user': {},
		'app_view_object': {'object': 1},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)



@login_required
def dashboard_creation(request):
	user_content_selected = aside_left_menu_includes.objects.filter(href='dashboard_publication', is_actual=True).first()

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
		app_events['actual'] = notification_events.objects.filter(is_actual=True, users_list=request.user, event_date__gte=confirm_events_user.confirm_date).all()
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
