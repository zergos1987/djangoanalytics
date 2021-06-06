from django.shortcuts import render, redirect



# Create your views here.
def index(request):

	template = 'app_zs_admin/index.html'
	breadcrumb_nav_active = {
		"breadcrumb_nav_active": "Home"
	}

	return render(request, template, breadcrumb_nav_active)

