from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse

from apps.app_zs_admin.models import app, aside_left_menu_includes
from custom_script_extensions.custom_permissions_check import check_user_content_request_permission


# Create your views here.
#@method_decorator([login_required, permission_required("app_opensource_dashboards.view_app")], name="dispatch")
@login_required
@permission_required('app_opensource_dashboards.view_app')
def index(request):
	app_settings = app.objects.filter(is_actual=True).first()
	app_opensource_dashboards_settings = ''
	
	template = 'app_opensource_dashboards/index.html' 
	context = {
		'app_settings': app_settings,
		'app_opensource_dashboards_settings': app_opensource_dashboards_settings
	}

	return render(request, template, context)


@login_required
@permission_required('app_opensource_dashboards.view_app')
def render_view(request, id):
	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=id,
		user_id=request.user.id)

	if not user_content_has_permission: raise PermissionDenied()

	app_settings = app.objects.filter(is_actual=True).first()
	app_opensource_dashboards_settings = ''
	
	template = 'app_zs_admin/render_view.html'

	context = {
		'app_settings': app_settings,
		'application_settings': app_opensource_dashboards_settings
	}

	return render(request, template, context)
