from django.core.management import call_command
from django.db import connections
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.db.models import Q
import logging



logger = logging.getLogger(__name__)



database_names = [
	'default', 
	'dash_sadko_postgres_db'
]

custom_permissionns = [
	{
		'app': 'app_zs_examples', 
		'permissions': [
			'dynamicTable_api_drf_get',
			'dynamicTable_api_drf_post',
			'dynamicTable_api_drf_put',
			'dynamicTable_api_drf_delete',
			'dynamicTable_api_drf_import',
			'dynamicTable_api_drf_export',
			'test_table_model_api_drf_get',
			'test_table_model_api_drf_post',
			'test_table_model_api_drf_put',
			'test_table_model_api_drf_delete',
			'test_table_model_api_drf_import',
			'test_table_model_api_drf_export',
		]
	},
]

default_admin = 'admin'
default_app_label = 'app_zs_admin'
read_only_app = ['app', 'accounts']
edit_only_app = ['auth', 'sessions']
users_default_password = '368696'

default_staff_users = ['TEST_USER_admin_viewer', 'TEST_USER_admin_editor', 'TEST_USER_admin_api']
default_users = ['TEST_USER_application_viewer', 'TEST_USER_application_editor', 'TEST_USER_application_api']

disintct_app_labels_staff = ['accounts', 'admin', 'auth', 'contenttypes', 'sessions']
distinct_app_labels_users = [] 


def create_default_users_groups_permissions():
	def create_user(user, is_staff):
		user, created = User.objects.get_or_create(username=user)
		if created:
			user.set_password(users_default_password)
			user.is_staff = is_staff
			user.save()

	def create_group(group):
		group, created = Group.objects.get_or_create(name=group)

	def add_user_to_group(user, group):
		group = Group.objects.get(name = group)
		user = User.objects.get(username=user)
		user.groups.add(group) 
		user.save()

	def create_permissions(app, group, perm_type):
		perms = None
		group = Group.objects.get(name=group)
		cts = ContentType.objects.filter(app_label=app)
		if perm_type == 'api':
			perms = Permission.objects.filter(Q(content_type__in=cts) & Q(Q(name__contains=perm_type) | (Q(content_type__model='app')) & Q(codename='view_app')))
		elif perm_type == 'viewer':
			perms = Permission.objects.filter(content_type__in=cts, name__contains=perm_type[:-2])
		elif perm_type == 'editor' and app in read_only_app:
			perms = Permission.objects.filter(content_type__in=cts, name__contains='view')
		elif perm_type == 'editor' and app in edit_only_app:
			perms = Permission.objects.filter(Q(content_type__in=cts) & ~Q(name__contains='delete'))
		elif perm_type == 'editor':
			perms = Permission.objects.filter(content_type__in=cts).exclude((Q(content_type__model='app')) & ~Q(codename='view_app'))
		if perms:
			group.permissions.add(*perms)
		return group

	def factory_user_perms_create(u, app, create_u=True, create_g=True, add_u_group=True, create_p=True, u_is_staff=False, default_group=None):
		app_user = app
		user_type = ''
		if not default_group: default_group = app
		#_api, _viewer, _editor etc..
		user_type = u[u.rfind('_'):]
		if 'TEST_USER' in u: app_user = 'TEST_USER_' + app + user_type
		if create_u: create_user(app_user, u_is_staff)
		#create user apps groups
		app_group = default_group + user_type + '_group'
		if create_g: create_group(app_group)
		#add user to group
		if add_u_group: add_user_to_group(app_user, app_group)
		#Create group permissions for user app
		if create_p: create_permissions(app, app_group, user_type[1:])
		
		
	#create custom permissions
	for app_perms in custom_permissionns:
		app = app_perms.get('app')
		perms = app_perms.get('permissions')
		content_type = ContentType.objects.get(app_label=app, model='app')
		for p in perms:
			obj, created = Permission.objects.get_or_create(codename=p, name=p, content_type=content_type)
	#get distinct user apps
	for i in Permission.objects.all():
		app_label = i.content_type.app_label
		if app_label not in distinct_app_labels_users and app_label not in disintct_app_labels_staff: distinct_app_labels_users.append(app_label)
	#create test users for user apps
	for app in distinct_app_labels_users:
		for u in default_users:
			factory_user_perms_create(u=u, app=app, create_u=True, create_g=True, add_u_group=True, create_p=True, u_is_staff=False, default_group=None)
	#create test staff groups and perms
	for app in disintct_app_labels_staff:
		for u in default_staff_users:
			factory_user_perms_create(u=u, app=app, create_u=False, create_g=True, add_u_group=False, create_p=True, u_is_staff=False, default_group='admin')
	#add applications perms for staff groups
	for app in distinct_app_labels_users:
		for u in default_staff_users:
			factory_user_perms_create(u=u, app=app, create_u=False, create_g=False, add_u_group=False, create_p=True, u_is_staff=False, default_group='admin')
	#create test staff users
	for u in default_staff_users:
		factory_user_perms_create(u=u, app='admin', create_u=True, create_g=False, add_u_group=True, create_p=False, u_is_staff=True, default_group=None)
	#add group perms to admin
	for u in default_staff_users:
		factory_user_perms_create(u=u.replace('TEST_USER_', ''), app='admin', create_u=False, create_g=False, add_u_group=True, create_p=False, u_is_staff=True, default_group=None)
	return 'Done.'





def initialize_management_commands():
	call_command('collectstatic', verbosity=0, interactive=False, link=True, clear=True)
	# call_command('makemigrations', app_label='accounts', database='default')
	# call_command('migrate', app_label='accounts', database='default')
	call_command('makemigrations')
	call_command('migrate')


def check_dbs_available():
	connection_status = []
	for db in database_names:

		conn = connections['default']
		try:
			c = conn.cursor() #this will take some time if error
		except OperationalError:
			reachable = False
		else:
			reachable = True
		connection_status.append({db:reachable})

	return connection_status


def initialize(django_initialize_management_commands=True, django_initialize_defaults=True):
	if django_initialize_management_commands: 
		initialize_management_commands()
		logger.debug(f'initialize_management_commands: done.')

	if django_initialize_defaults:
		# check if defaut database was load
		is_dbs_available = check_dbs_available()
		if [d for d in is_dbs_available if 'default' in d][0].get('default', False):
			create_default_users_groups_permissions_status = create_default_users_groups_permissions()
		# 	is_default_groups_exists_or_create = check_default_groups_exists_or_create()
		# 	is_default_user_roles_exists_or_create = create_default_user_roles_exists_or_create()

		logger.debug(f'is_dbs_available: {is_dbs_available}')
		logger.debug(f'create_default_users_groups_permissions: {create_default_users_groups_permissions_status}')
		logger.debug(f'django_initialize_defaults: done.')
		
	logger.debug(f'initialize: done.')


