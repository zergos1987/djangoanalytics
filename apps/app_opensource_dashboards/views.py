from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.urls import reverse
import os
from decouple import config

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
		'app_settings_user': {},
		'app_opensource_dashboards_settings': app_opensource_dashboards_settings,
		'app_opensource_dashboards_settings_user': {}
	}

	return render(request, template, context)


# internal views ################################################################
OS_DASHBOARDS_METABASE_URL = os.environ.get("OS_DASHBOARDS_METABASE_URL", config('OS_DASHBOARDS_METABASE_URL'))
OS_DASHBOARDS_METABASE_SECRET_KEY = os.environ.get("OS_DASHBOARDS_METABASE_SECRET_KEY", config('OS_DASHBOARDS_METABASE_SECRET_KEY'))
OS_DASHBOARDS_METABASE_LOGIN = os.environ.get("OS_DASHBOARDS_METABASE_LOGIN", config('OS_DASHBOARDS_METABASE_LOGIN'))
OS_DASHBOARDS_METABASE_PSW = os.environ.get("OS_DASHBOARDS_METABASE_PSW", config('OS_DASHBOARDS_METABASE_PSW'))


def get_metabase_api(ask=None):
	from metabase_api import Metabase_API
	import requests
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

	def authenticate(self):
		"""Get a Session ID"""
		conn_header = {'username':self.email, 'password':self.password}
		res = requests.post(self.domain + '/api/session', json=conn_header, auth=self.auth, verify=False)
		if not res.ok: raise Exception(res)
		self.session_id = res.json()['id']
		self.header = {'X-Metabase-Session':self.session_id}
	def validate_session(self):
		"""Get a new session ID if the previous one has expired"""
		res = requests.get(self.domain + '/api/user/current', headers=self.header, auth=self.auth, verify=False)
		if res.ok: 
			return True
		elif res.status_code == 401: 
			return self.authenticate()
		else: 
			raise Exception(res)
	def get(self, endpoint, *args, **kwargs):
		self.validate_session()
		res = requests.get(self.domain + endpoint, headers=self.header, **kwargs, auth=self.auth, verify=False)
		if 'raw' in args:
			return res
		else:
			return res.json() if res.ok else False
	def post(self, endpoint, *args, **kwargs):
		self.validate_session()
		res = requests.post(self.domain + endpoint, headers=self.header, **kwargs, auth=self.auth, verify=False)
		if 'raw' in args:
			return res
		else:
			return res.json() if res.ok else False
	def put(self, endpoint, *args, **kwargs):
		"""Used for updating objects (cards, dashboards, ...)"""
		self.validate_session()
		res = requests.put(self.domain + endpoint, headers=self.header, **kwargs, auth=self.auth, verify=False)
		if 'raw' in args:
			return res
		else:
			return res.status_code
	def delete(self, endpoint, *args, **kwargs):
		self.validate_session()
		res = requests.delete(self.domain + endpoint, headers=self.header, **kwargs, auth=self.auth, verify=False)
		if 'raw' in args:
			return res
		else:
			return res.status_code

	Metabase_API.authenticate = authenticate
	Metabase_API.validate_session = validate_session
	Metabase_API.get = get
	Metabase_API.post = post
	Metabase_API.put = put
	Metabase_API.delete = delete

	if ask == 'dashboards_list':
		mb = Metabase_API(
			OS_DASHBOARDS_METABASE_URL, 
			OS_DASHBOARDS_METABASE_LOGIN,
			OS_DASHBOARDS_METABASE_PSW
			)
		ask = mb.get('/api/dashboard/embeddable')
	return ask


def get_metabase_iframe(dashboard_id=None):
	if not dashboard_id: return '#'

	import jwt
	import time

	METABASE_SITE_URL = OS_DASHBOARDS_METABASE_URL
	METABASE_SECRET_KEY = OS_DASHBOARDS_METABASE_SECRET_KEY

	payload = {
	  "resource": {"dashboard": dashboard_id},
	  "params": {
	    "дата_начала_пм": "2021-07-01~2021-07-15",
	    #"yeardatatermstats": "2020;2021",
	  },
	  "exp": round(time.time()) + (60 * 10) # 10 minute expiration
	}
	token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

	iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=false&titled=false"
	return iframeUrl


@login_required
@permission_required('app_opensource_dashboards.view_app')
def mb(request, id):
	user_content_selected = aside_left_menu_includes.objects.filter(id=id, is_actual=True).first()

	user_content_has_permission = check_user_content_request_permission(
		content_obj='aside_left_menu_includes',
		obj_id=user_content_selected.id,
		user_id=request.user.id)
	if not user_content_has_permission: raise PermissionDenied()

	dashboards_list = []
	try:
		dashboards_list = get_metabase_api(ask='dashboards_list')
	except Exception as e:
		print('dashboards_list error: ', str(e))
	selected_metabase_dashboard_id = [i for i in dashboards_list if i.get('name') == user_content_selected.external_href]

	app_view_object = {}
	if selected_metabase_dashboard_id: 
		selected_metabase_dashboard_id = selected_metabase_dashboard_id[0].get('id')
		app_view_object = {'object': get_metabase_iframe(dashboard_id=selected_metabase_dashboard_id)}
		app_view_object['object_html_source'] = {'css': ['static/app_opensource_dashboards/origin/css/metabase_zs_admin.css'], 'js': []}

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
	context['app_view_object'] = app_view_object

	return render(request, template, context)
