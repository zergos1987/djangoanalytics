from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse

from apps.app_zs_admin.models import app, aside_left_menu_includes



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
	content_access = True

	user_selected_content = aside_left_menu_includes.objects.get(id=id)

	required_user_check = user_selected_content.url_access_via_users.all()
	required_user_check_count = len(required_user_check)
	required_groups_check = user_selected_content.url_access_via_groups.all()
	required_groups_check_count = len(required_groups_check)

	user_matches = [val for val in required_user_check if val.username in [request.user.username]]
	groups_matches = [val for val in required_groups_check if val in request.user.groups.all()]

	if len(user_matches) == 1 and required_user_check_count > 0: content_access = False
	if len(groups_matches) != required_groups_check_count: content_access = False



	print(content_access, 'FFFFFFFF', required_groups_check, required_user_check)
	print(content_access, 'YYYYYYYY', groups_matches, user_matches)

	app_settings = app.objects.filter(is_actual=True).first()
	app_opensource_dashboards_settings = ''
	
	template = 'app_opensource_dashboards/index.html'

	context = {
		'app_settings': app_settings,
		'app_opensource_dashboards_settings': app_opensource_dashboards_settings
	}
	content_access = False
	# if content_access == False:
	# 	return HttpResponseRedirect(reverse('app_zs_admin:403'))

	# from django.http import Http404
	# raise Http404("Poll does not exist")
	raise Http404()

	return render(request, template, context)
