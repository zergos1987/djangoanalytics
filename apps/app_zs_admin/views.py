from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse

from apps.app_zs_admin.models import app, aside_left_menu_includes
from custom_script_extensions.custom_permissions_check import check_user_content_request_permission




# Create your views here.
#@method_decorator([login_required, permission_required("app_zs_admin.view_app")], name="dispatch")
@login_required
#@permission_required('app_zs_admin.view_app')
def index(request):
	app_settings = app.objects.filter(is_actual=True).first()
	if 'zs_admin' != app_settings.app_start_page:
		return HttpResponseRedirect(f'/{app_settings.app_start_page}/')
	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
	}

	template = 'app_zs_admin/index.html' 

	return render(request, template, context)


@login_required
@permission_required('app_zs_admin.view_app')
def settings_index(request):
	app_settings = app.objects.filter(is_actual=True).first()

	context = {
		'app_settings': app_settings,
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
		print('internal', user_content_selected.href)
		return redirect(reverse(f"{user_content_selected.source_app_name}:{user_content_selected.href}"))
		#return redirect('{}?flag=True&user_id=23'.format(reverse(f"{user_content_selected.render_app_name}:{user_content_selected.href}")))
	if content_source_type == 'external':
		print('external', user_content_selected.href)

	#raise Http404()

	app_settings = app.objects.filter(is_actual=True).first()
	template = 'app_zs_admin/render_view.html'
	context = {
		'app_settings': app_settings,
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
	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/400.html", context)
	response.status_code = 400
	return response


@login_required
#@permission_required('app_zs_admin.view_app')
def handler403(request, exception):
	app_settings = app.objects.filter(is_actual=True).first()
	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/403.html", context)
	response.status_code = 403
	return response


@login_required
#@permission_required('app_zs_admin.view_app')
def handler404(request, exception):
	app_settings = app.objects.filter(is_actual=True).first()
	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/404.html", context)
	response.status_code = 404
	return response


@login_required
#@permission_required('app_zs_admin.view_app')
def handler500(request):
	app_settings = app.objects.filter(is_actual=True).first()
	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
	}
	response = render(request, "app_zs_admin/500.html", context)
	response.status_code = 500
	return response


# internal views ################################################################
def users_profile(request):
	user_content_selected = aside_left_menu_includes.objects.filter(href='users_profile', is_actual=True).first()

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
	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
		'app_view_object': {'object': 1},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)


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
	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
		'app_view_object': {'object': 1},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)


def dashboard_publication(request):
	user_content_selected = aside_left_menu_includes.objects.filter(href='dashboard_publication', is_actual=True).first()

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
	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'app_settings_user': {},
		'app_view_object': {'object': 1},
		'app_view_object_settings': user_content_selected,
		'app_view_settings': {},
		'app_view_settings_user': {},
	}

	return render(request, template, context)
