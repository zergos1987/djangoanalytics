from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.contrib.auth.models import User, Group
from django.views.generic import UpdateView, ListView, TemplateView, RedirectView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Case, Sum, Min, Max, Count, When, Q, F, Value, IntegerField, CharField, DateField, DateTimeField
#from .models import zs_dashboards_Users
from custom_script_extensions.group_permission_check import user_group_access_check

import uuid
from django.utils.crypto import get_random_string

from datetime import datetime
import json

import os



@login_required
@user_group_access_check('app_opensource_surveys')
def index(request):

	template = 'app_opensource_surveys/index.html'

	return render(request, template)
