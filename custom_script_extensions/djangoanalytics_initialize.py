from django.core.management import call_command
from django.db import connections
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.db.models import Q
import operator
from functools import reduce
import logging



logger = logging.getLogger(__name__)



database_names = [
	'default', 
	'dash_sadko_postgres_db'
]
custom_permissionns = [
	{
		'app': 'app_zs_examples', 
		'model': 'app',
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
	}, {
		'app': 'accounts',
		'model': 'app',
		'permissions': [
			'can_ban_users',
			'can_unban_users',
		]
	}
]





perm_view_app_list = [
	'app', 'auth', 'accounts', 'admin', 
	'sessions', 'contenttypes'
]
app_list = []
for i in Permission.objects.all():
	if i.content_type.app_label not in app_list: 
		if i.content_type.app_label not in perm_view_app_list:
			app_list.append(i.content_type.app_label) 

perm_create_app_list = []
perm_update_app_list = []
perm_delete_app_list = []

perm_custom_app_list = ['all']

perm_view_model_list = [
	'app', 'sessions.Session', 'auth.Group', 'auth.User', 
	'contenttypes.ContentType', 'accounts.AuditEntry', 'accounts.UserSession'
]
perm_create_model_list = ['User']
perm_update_model_list = ['User']
perm_delete_model_list = []

perm_custom_model_list = ['app']

role_groups = [
	'admin_viewer', 'admin_editor', 'admin_creator', 'admin_api', 
	'Application_viewer', 'Application_editor', 'Application_creator', 'Application_api'
]

default_users = ['admin', 'TEST_USER']
default_password = '368696'

def create_default_users_groups_permissions():
	#create user if not exists
	def get_or_create_user(u, is_staff=False):
		obj, created = User.objects.get_or_create(username=u)
		if created:
			obj.set_password(default_password)
			obj.is_staff = is_staff
			obj.save()
		print('STATUS. create user if not exists:', created, obj)

	for u in default_users:
		is_staff = False
		if u == 'admin': get_or_create_user(u, True)
		if u == 'TEST_USER':
			for r in role_groups:
				if 'Application' in r:
					for app in app_list:
						u_via_r = u + '_' + app + r.replace('Application', '')
						get_or_create_user(u_via_r, is_staff)
				else:
					is_staff = True
					u_via_r = u + '_' + r
					get_or_create_user(u_via_r, is_staff)


	#create permissions if not exists
	def get_or_create_permission(codename, name, content_type):
		obj, created = Permission.objects.get_or_create(codename=codename, name=name, content_type=content_type)
		print('STATUS. create permissions if not exists:', created, obj)

	for p_data in custom_permissionns:
		app = p_data.get('app')
		model = p_data.get('model')
		permission_list = p_data.get('permissions')
		content_type = ContentType.objects.get(app_label=app, model=model)
		for p in permission_list:
			get_or_create_permission(codename=p, name=p, content_type=content_type)


	#create groups if not exists
	def get_or_create_groups(g):
		obj, created = Group.objects.get_or_create(name=g)
		print('STATUS. create groups if not exists:', created, obj)

	for g in role_groups:
		if 'Application' in g:
			for a in app_list:
				get_or_create_groups(g.replace('Application', a) + '_group')
		else:
			get_or_create_groups(g + '_group')


	#add permissions to groups if not exists
	def get_or_create_add_permission_to_group(group_name, app_name, perm_type):
		g = Group.objects.get(name=group_name)
		cts_list = []
		if type(app_name).__name__ == 'list':
			for app in app_name:
				cts_list.append(ContentType.objects.filter(app_label=app))
		if type(app_name).__name__ == 'str':
			cts_list.append(ContentType.objects.filter(app_label=app))

		for cts in cts_list:
			for p_type in perm_type:
				p = Permission.objects.filter(content_type__in=cts, name__contains=p_type)
				if p: 
					g.permissions.add(*p)
				print('STATUS. add permissions to groups if not exists:', len(p))

	actual_g_list = Group.objects.all()
	for g in actual_g_list:
		group_name = g.name
		app_name = group_name[:group_name.find('_')]
		if app_name == 'admin': 
			app_name = app_list
		else:
			app_name = group_name[:group_name.replace('_group', '').rfind('_')]
		print(group_name, app_name)
		# if 'viewer' in group_name:
		# 	get_or_create_add_permission_to_group(group_name, app_name, ['view_'])
		# elif 'editor' in group_name:
		# 	get_or_create_add_permission_to_group(group_name, app_name, ['change_', ''])
		# elif 'creator' in group_name:
		# 	get_or_create_add_permission_to_group(group_name, app_name, ['add_', 'delete_'])
		# elif 'api' in group_name:
		# 	get_or_create_add_permission_to_group(group_name, app_name, ['api_'])
		# else:
		# 	get_or_create_add_permission_to_group(group_name, app_name, 'nnnn')


	# #add groups to users if not exists
	# def get_or_create_add_groups_to_users(username, groupname):
	# 	group = Group.objects.get(name=groupname)
	# 	user = User.objects.get(username=username)
	# 	user.groups.add(group) 
	# 	user.save()
	# 	print('STATUS. add groups to users if not exists:', user, group)


	# conditions = reduce(operator.or_, [Q(**{"username__contains": user}) for user in default_users])
	# actual_u_list = User.objects.filter(conditions)
	# for u in actual_u_list:
	# 	username = u.username
	# 	groupname = username[username.find('_USER_')+6:] + '_group'
	# 	get_or_create_add_groups_to_users(username, groupname)

	return 'Done.'


# custom_permissionns = [
# 	{
# 		'app': 'app_zs_examples', 
# 		'permissions': [
# 			'dynamicTable_api_drf_get',
# 			'dynamicTable_api_drf_post',
# 			'dynamicTable_api_drf_put',
# 			'dynamicTable_api_drf_delete',
# 			'dynamicTable_api_drf_import',
# 			'dynamicTable_api_drf_export',
# 			'test_table_model_api_drf_get',
# 			'test_table_model_api_drf_post',
# 			'test_table_model_api_drf_put',
# 			'test_table_model_api_drf_delete',
# 			'test_table_model_api_drf_import',
# 			'test_table_model_api_drf_export',
# 		]
# 	}, {
# 		'app': 'accounts',
# 		'permissions': [
# 			'can_ban_users',
# 			'can_unban_users',
# 		]
# 	}
# ]

# default_admin = 'admin'
# default_app_label = 'app_zs_admin'
# read_only_app = ['app', 'auth', 'accounts', 'sessions']
# edit_only_app = []
# users_default_password = '368696'

# default_staff_users = ['TEST_USER_admin_viewer', 'TEST_USER_admin_editor', 'TEST_USER_admin_api']
# default_users = ['TEST_USER_application_viewer', 'TEST_USER_application_editor', 'TEST_USER_application_api']

# disintct_app_labels_staff = ['accounts', 'admin', 'auth', 'contenttypes']
# distinct_app_labels_users = [] 


# def create_default_users_groups_permissions():
# 	def create_user(user, is_staff):
# 		user, created = User.objects.get_or_create(username=user)
# 		if created:
# 			user.set_password(users_default_password)
# 			user.is_staff = is_staff
# 			user.save()

# 	def create_group(group):
# 		group, created = Group.objects.get_or_create(name=group)

# 	def add_user_to_group(user, group):
# 		group = Group.objects.get(name = group)
# 		user = User.objects.get(username=user)
# 		user.groups.add(group) 
# 		user.save()

# 	def create_permissions(app, group, perm_type):
# 		perms = None
# 		group = Group.objects.get(name=group)
# 		cts = ContentType.objects.filter(app_label=app)
# 		if perm_type == 'api':
# 			perms = Permission.objects.filter(Q(content_type__in=cts) & Q(Q(name__contains=perm_type) | (Q(content_type__model='app')) & Q(codename='view_app')))
# 		elif perm_type == 'viewer':
# 			perms = Permission.objects.filter(content_type__in=cts, name__contains=perm_type[:-2])
# 		elif perm_type == 'editor' and app in read_only_app:
# 			perms = Permission.objects.filter(content_type__in=cts, name__contains='view')
# 		elif perm_type == 'editor' and app in edit_only_app:
# 			perms = Permission.objects.filter(Q(content_type__in=cts) & ~Q(name__contains='delete'))
# 		elif perm_type == 'editor':
# 			perms = Permission.objects.filter(content_type__in=cts).exclude((Q(content_type__model='app')) & ~Q(codename='view_app'))
# 		if perms:
# 			group.permissions.add(*perms)
# 		return group

# 	def factory_user_perms_create(u, app, create_u=True, create_g=True, add_u_group=True, create_p=True, u_is_staff=False, default_group=None):
# 		app_user = app
# 		user_type = ''
# 		if not default_group: default_group = app
# 		#_api, _viewer, _editor etc..
# 		user_type = u[u.rfind('_'):]
# 		if 'TEST_USER' in u: app_user = 'TEST_USER_' + app + user_type
# 		if create_u: create_user(app_user, u_is_staff)
# 		#create user apps groups
# 		app_group = default_group + user_type + '_group'
# 		if create_g: create_group(app_group)
# 		#add user to group
# 		if add_u_group: add_user_to_group(app_user, app_group)
# 		#Create group permissions for user app
# 		if create_p: create_permissions(app, app_group, user_type[1:])
		
		
# 	#create custom permissions
# 	for app_perms in custom_permissionns:
# 		app = app_perms.get('app')
# 		perms = app_perms.get('permissions')
# 		content_type = ContentType.objects.get(app_label=app, model='app')
# 		for p in perms:
# 			obj, created = Permission.objects.get_or_create(codename=p, name=p, content_type=content_type)
# 	#get distinct user apps
# 	for i in Permission.objects.all():
# 		app_label = i.content_type.app_label
# 		if app_label not in distinct_app_labels_users and app_label not in disintct_app_labels_staff: distinct_app_labels_users.append(app_label)
# 	#create test users for user apps
# 	for app in distinct_app_labels_users:
# 		for u in default_users:
# 			factory_user_perms_create(u=u, app=app, create_u=True, create_g=True, add_u_group=True, create_p=True, u_is_staff=False, default_group=None)
# 	#create test staff groups and perms
# 	for app in disintct_app_labels_staff:
# 		for u in default_staff_users:
# 			factory_user_perms_create(u=u, app=app, create_u=False, create_g=True, add_u_group=False, create_p=True, u_is_staff=False, default_group='admin')
# 	#add applications perms for staff groups
# 	for app in distinct_app_labels_users:
# 		for u in default_staff_users:
# 			factory_user_perms_create(u=u, app=app, create_u=False, create_g=False, add_u_group=False, create_p=True, u_is_staff=False, default_group='admin')
# 	#create test staff users
# 	for u in default_staff_users:
# 		factory_user_perms_create(u=u, app='admin', create_u=True, create_g=False, add_u_group=True, create_p=False, u_is_staff=True, default_group=None)
# 	#add group perms to admin
# 	for u in default_staff_users:
# 		factory_user_perms_create(u=u.replace('TEST_USER_', ''), app='admin', create_u=False, create_g=False, add_u_group=True, create_p=False, u_is_staff=True, default_group=None)
# 	return 'Done.'


def initialize_management_commands():
	call_command('collectstatic', verbosity=0, interactive=False, link=False, clear=True)
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



