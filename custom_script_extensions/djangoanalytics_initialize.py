from django.core.management import call_command
from django.db import connections
from django.contrib.auth.models import User, Group, Permission, ContentType
from apps.accounts.models import user_extra_details
from django.db.models import Q
import operator
from functools import reduce
import logging
import sys
import os




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



staff_perm_view_app_list = [
	'app', 'auth', 'accounts', 'admin', 
	'sessions', 'contenttypes'
]
app_list = []
for i in Permission.objects.all():
	if i.content_type.app_label not in app_list: 
		if i.content_type.app_label not in staff_perm_view_app_list:
			app_list.append(i.content_type.app_label) 

staff_perm_create_app_list = []
staff_perm_update_app_list = []
staff_perm_delete_app_list = []

perm_custom_app_list = ['all']

staff_perm_view_model_list = [
	'app', 'sessions.Session', 'auth.Group', 'auth.User', 
	'contenttypes.ContentType', 'accounts.AuditEntry', 'accounts.UserSession'
]
staff_perm_create_model_list = ['User']
staff_perm_update_model_list = ['User']
staff_perm_delete_model_list = []

perm_custom_model_list = ['app']

role_groups = [
	'admin_viewer', 'admin_editor', 'admin_creator', 'admin_api', 
	'Application_viewer', 'Application_editor', 'Application_creator', 'Application_api'
]

default_users = ['admin', 'TEST_USER']
default_password = '368696'




#create user if not exists
def get_or_create_user(u, is_staff=False):
	obj, created = User.objects.get_or_create(username=u)
	if created:
		obj.set_password(default_password)
		obj.is_staff = is_staff
		obj.save()
	print('STATUS. create user if not exists:', created, obj)


#create permissions if not exists
def get_or_create_permission(codename, name, content_type):
	obj, created = Permission.objects.get_or_create(codename=codename, name=name, content_type=content_type)
	print('STATUS. create permissions if not exists:', created, obj)


#create groups if not exists
def get_or_create_groups(g):
	obj, created = Group.objects.get_or_create(name=g)
	print('STATUS. create groups if not exists:', created, obj)


#add permissions to groups if not exists
def add_permission_to_group(group_name, app_name, perm_type):
	g = Group.objects.get(name=group_name)
	cts_list = []
	if type(app_name).__name__ == 'list':
		for app in app_name:
			cts_list.append(ContentType.objects.filter(app_label=app))
	if type(app_name).__name__ == 'str':
		cts_list.append(ContentType.objects.filter(app_label=app_name))

	for cts in cts_list:
		for p_type in perm_type:
			p = Permission.objects.filter(content_type__in=cts, codename__contains=p_type)
			if p: 
				g.permissions.add(*p)
			print('STATUS. add permissions to groups if not exists:', len(p))


#add groups to users if not exists
def add_groups_to_users(username, groupname):
	group = Group.objects.get(name=groupname)
	user = User.objects.get(username=username)
	user.groups.add(group) 
	user.save()
	#print('STATUS. add groups to users if not exists:', user, group)


#update user groups
def update_user_groups(username, update_group_list, filter_contains):
    user = User.objects.get(username=username)
    user_groups = user.groups.filter(name__contains=filter_contains)
    for g in list(user_groups):
        if g.name not in update_group_list:
            user.groups.remove(g)


#update user extra data
def update_user_extra_data(username, extra_data):
	def get_update_value(search_field):
		v = [i for i in extra_data if search_field in i][0].get(search_field, None)#[0]
		if type(v).__name__ != 'bool': v = v[0]
		return v

	user = User.objects.get(username=username)
	u, created = user_extra_details.objects.get_or_create(user=user)
	u.full_name = get_update_value('full_name')
	u.department = get_update_value('department')
	u.center = get_update_value('center')
	u.position = get_update_value('position')
	u.name = get_update_value('name')
	u.last_name = get_update_value('last_name')
	u.ldap_is_active = get_update_value('ldap_is_active')
	u.save()
	
	if u.ldap_is_active == False:
		u.is_active = False
		u.save()



def create_default_users_groups_permissions():
	#create user if not exists
	for u in default_users:
		is_staff = False
		if u == 'admin': get_or_create_user(u=u, is_staff=True)
		if u == 'TEST_USER':
			for r in role_groups:
				if 'Application' in r:
					for app in app_list:
						u_via_r = u + '_' + app + r.replace('Application', '')
						get_or_create_user(u=u_via_r, is_staff=False)
				if r[:5] == 'admin':
					u_via_r = u + '_' + r
					get_or_create_user(u=u_via_r, is_staff=True)


	#create permissions if not exists
	for p_data in custom_permissionns:
		app = p_data.get('app')
		model = p_data.get('model')
		permission_list = p_data.get('permissions')
		content_type = ContentType.objects.get(app_label=app, model=model)
		for p in permission_list:
			get_or_create_permission(codename=p, name=p, content_type=content_type)
	

	#create groups if not exists
	for g in role_groups:
		if 'Application' in g:
			for a in app_list:
				get_or_create_groups(g.replace('Application', a) + '_group')
		else:
			get_or_create_groups(g + '_group')


	#add permissions to groups if not exists
	actual_g_list = Group.objects.all()
	for g in actual_g_list:
		#print('1========', g.name)
		#print('2========', g.name[:g.name.find('_')], g.name[:g.name.replace('_group', '').rfind('_')])
		group_name = g.name
		app_name = group_name[:group_name.find('_')]
		if app_name == 'admin': 
			app_name = app_list + staff_perm_view_app_list
		else:
			app_name = group_name[:group_name.replace('_group', '').rfind('_')]
		if 'viewer' in group_name:
			add_permission_to_group(group_name, app_name, ['view_'])
		elif 'editor' in group_name:
			add_permission_to_group(group_name, app_name, ['change_'])
		elif 'creator' in group_name:
			add_permission_to_group(group_name, app_name, ['delete_', 'add_'])
		elif 'api' in group_name:
			add_permission_to_group(group_name, app_name, ['api_'])
		# else:
		# 	add_permission_to_group(group_name, app_name, 'nnnn')


	conditions = reduce(operator.or_, [Q(**{"username__contains": user}) for user in default_users])
	actual_u_list = User.objects.filter(conditions)
	for u in actual_u_list:
		if 'TEST_USER' in u.username:
			username = u.username
			groupname = username[username.find('_USER_')+6:] + '_group'
			#print('===', username, groupname)
			add_groups_to_users(username, groupname)
			if 'editor' in groupname or 'creator' in groupname or 'api' in groupname:
				groupname = groupname.replace('editor', 'viewer').replace('creator', 'viewer').replace('api', 'viewer')
				add_groups_to_users(username, groupname)


	return 'Done.'





def initialize_management_commands():
	project_path = os.getcwd()
	# with open(project_path + '\\logs/django\\initialize_management_commands_check.log', 'w') as f:
	# 	call_command('check', verbosity=1, stdout=f)
	with open(project_path + '\\logs/django\\initialize_management_commands_collectstatic.log', 'w') as f:
		call_command('collectstatic', verbosity=1, interactive=False, link=False, clear=True, stdout=f)
	with open(project_path + '\\logs/django\\initialize_management_commands_makemigrations.log', 'w') as f:
		call_command('makemigrations', verbosity=1, stdout=f)
	with open(project_path + '\\logs/django\\initialize_management_commands_migrate.log', 'w') as f:
		call_command('migrate', verbosity=1, stdout=f)
	#python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"


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
		logger.info(f'initialize_management_commands: done.')

	if django_initialize_defaults:
		# check if defaut database was load
		is_dbs_available = check_dbs_available()
		if [d for d in is_dbs_available if 'default' in d][0].get('default', False):
			create_default_users_groups_permissions_status = create_default_users_groups_permissions()
		# 	is_default_groups_exists_or_create = check_default_groups_exists_or_create()
		# 	is_default_user_roles_exists_or_create = create_default_user_roles_exists_or_create()

		logger.info(f'is_dbs_available: {is_dbs_available}')
		logger.info(f'create_default_users_groups_permissions: {create_default_users_groups_permissions_status}')
		logger.info(f'django_initialize_defaults: done.')
		
	logger.info(f'initialize: done.')
