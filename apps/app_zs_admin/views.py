from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):

	template = 'app_zs_admin/index.html'
	breadcrumb_nav_active = {
		"breadcrumb_nav_active": "Home"
	}

	return render(request, template, breadcrumb_nav_active)

