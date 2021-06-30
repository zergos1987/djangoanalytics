from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect


from apps.app_zs_admin.models import app



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
	print(id, 'QQQQQQQQQQQQQQQ')

	app_settings = app.objects.filter(is_actual=True).first()
	app_opensource_dashboards_settings = ''
	
	template = 'app_opensource_dashboards/index.html'

	context = {
		'app_settings': app_settings,
		'app_opensource_dashboards_settings': app_opensource_dashboards_settings
	}

	return render(request, template, context)
