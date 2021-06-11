from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.contrib.auth.models import User, Group
from django.views.generic import UpdateView, ListView, TemplateView, RedirectView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Case, Sum, Min, Max, Count, When, Q, F, Value, IntegerField, CharField, DateField, DateTimeField

import uuid
from django.utils.crypto import get_random_string

from datetime import datetime
import json

import os


# Create your views here.
#@method_decorator([login_required, permission_required("app_zs_admin.can_view_app")], name="dispatch")
@login_required
@permission_required('app_zs_admin.can_view_app')
def index(request):

	template = 'app_zs_admin/index.html'
	breadcrumb_nav_active = {
		"breadcrumb_nav_active": "Home"
	}

	return render(request, template, breadcrumb_nav_active)

