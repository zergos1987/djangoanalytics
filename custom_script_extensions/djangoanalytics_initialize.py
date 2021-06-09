from django.core.management import call_command
from django.db import connections
from django.contrib.auth.models import User, Group, Permission, ContentType
import logging



logger = logging.getLogger(__name__)



database_names = [
	'default', 
	'dash_sadko_postgres_db'
]
group_permissions = [
	{
		'role_groups__id': 1,
		'app_label': ['accounts', 'admin'],
		'model': None,
		'permissions': None,
	},{
		'role_groups__id': 1,
		'app_label': ['auth', 'contenttypes', 'sessions'],
		'model': None,
		'permissions': ['Can view group', 'Can view permission', 'Can view user', 'Can view content type', 'Can view session'],
	},
]
role_groups = [
	{1: 'admin_permissions'}
	{2: 'accounts'}, 
	{3: 'app_opensource_dashboards'}, 
	{4: 'app_opensource_surveys'},
	{5: 'app_zs_admin'},
	{6: 'app_zs_dashboards'},
	{7: 'app_zs_examples'},
	{8: 'database_oracle_sadko'},
	{9: 'database_sqlite_test'},
	{70001: 'app_zs_examples__genericTable__drf__get'},
	{70002: 'app_zs_examples__genericTable__drf__post'},
	{70003: 'app_zs_examples__genericTable__drf__put'},
	{70004: 'app_zs_examples__genericTable__drf__delete'},
	{70005: 'app_zs_examples__genericTable__drf__export'},
	{70006: 'app_zs_examples__genericTable__drf__import'},
	{70007: 'app_zs_examples__test_table_model__drf__get'},
	{70008: 'app_zs_examples__test_table_model__drf__post'},
	{70009: 'app_zs_examples__test_table_model__drf__put'},
	{70010: 'app_zs_examples__test_table_model__drf__delete'},
	{70011: 'app_zs_examples__test_table_model__drf__export'},
	{70012: 'app_zs_examples__test_table_model__drf__import'},
]
user_roles = [
	{
		'admin_ROLE': {
			'user_groups': [
				'admin_permissions_ROLE',
				'api_ROLE', 
				'staff_ROLE',
				'accounts_ROLE',
				'app_opensource_dashboards_ROLE',
				'app_opensource_surveys_ROLE',
				'app_zs_admin_ROLE',
				'app_zs_dashboards_ROLE',
				'app_zs_examples_ROLE',
				'database_oracle_sadko_ROLE',
				'database_sqlite_test_ROLE',
			], 
			'is_staff': [True]
		}
	},{
		'api_ROLE': {
			'user_groups': ['app_zs_examples_ROLE'], 
			'is_staff': [False]
		}
	},{
		'staff_ROLE': {
			'user_groups': ['accounts_ROLE'], 
			'is_staff': [True]
		}
	},{
		'admin_permissions_ROLE': {
			'user_groups': [1], 
			'is_staff': [False]
		}
	},{
		'accounts_ROLE': {
			'user_groups': [2], 
			'is_staff': [False]
		}
	},{
		'app_opensource_dashboards_ROLE': {
			'user_groups': [3], 
			'is_staff': [False]
		}
	},{
		'app_opensource_surveys_ROLE': {
			'user_groups': [4], 
			'is_staff': [False]
		}
	},{
		'app_zs_admin_ROLE': {
			'user_groups': [5], 
			'is_staff': [False]
		}
	},{
		'app_zs_dashboards_ROLE': {
			'user_groups': [6], 
			'is_staff': [False]
		}
	},{
		'app_zs_examples_ROLE': {
			'user_groups': [7, 70001, 70002, 70003, 70004, 70005, 70006, 70007, 70008, 70009, 70009, 70010, 70011, 70012], 
			'is_staff': [False]
		}
	},{
		'database_oracle_sadko_ROLE': {
			'user_groups': [8], 
			'is_staff': [False]
		}
	},{
		'database_sqlite_test_ROLE': {
			'user_groups': [9], 
			'is_staff': [False]
		}
	},
]
users = [
	{
		'admin': {
			'roles': ['admin_ROLE'],
		}
	},{
		'TEST_USER_admin': {
			'roles': ['admin_ROLE'],
		}
	},{
		'TEST_USER_api_user': {
			'roles': ['api_ROLE'],
		}
	},{
		'TEST_USER_staff': {
			'roles': ['staff_ROLE'],
		}
	},{
		'TEST_USER_accounts': {
			'roles': ['accounts_ROLE'],
		}
	},{
		'TEST_USER_app_opensource_dashboards': {
			'roles': ['app_opensource_dashboards_ROLE'],
		}
	},{
		'TEST_USER_app_opensource_surveys': {
			'roles': ['app_opensource_surveys_ROLE'],
		}
	},{
		'TEST_USER_app_zs_admin': {
			'roles': ['app_zs_admin_ROLE'],
		}
	},{
		'TEST_USER_database_oracle_sadko': {
			'roles': ['database_oracle_sadko_ROLE'],
		}
	},{
		'TEST_USER_database_sqlite_test': {
			'roles': ['database_sqlite_test_ROLE'],
		}
	}
]
users_default_password = '368696'





def init_django_commands():
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


def check_default_groups_exists_or_create():
	group_status = []
	for g in role_groups:
		g = list(g.values())[0]
		g_status = Group.objects.filter(name=g).first()
		if g_status is None: 
			g_status = False
			Group.objects.create(name=g)
			#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
			# for i in Permission:
			# 	print(i.content_type.app_label, i.content_type.model, i.id, i.name)
		else:
			g_status = True
		group_status.append({g:g_status})
	return group_status


def create_default_user_roles_exists_or_create():

	created_users_and_roles = []

	def get_role_groups(role):
		tmp_groups = []
		for r in user_roles:
			r_key = list(r.keys())[0]
			if r_key == role:
				r_parameters = r.get(r_key, False)
				r_group_list = r_parameters.get('user_groups', False)
				for g in r_group_list:
					if isinstance(g, str): 
						for j in get_role_groups(g):
							tmp_groups.append(j)
					else:
						tmp_groups.append(g)
		return tmp_groups


	for u in users:
		u_key = list(u.keys())[0]
		u_parameters = u.get(u_key, False)
		u_role_list = u_parameters.get('roles', False)

		u_role_groups = []
		r_is_staff = False
		
		for role in u_role_list:
			for r in user_roles:
				r_key = list(r.keys())[0]
				if role == r_key:
					r_parameters = r.get(r_key, False)
					r_group_list = r_parameters.get('user_groups', False)
					r_is_staff = r_parameters.get('is_staff', False)
					for g in r_group_list:
						if isinstance(g, str): 
							for g2 in get_role_groups(g):
								if g2 not in u_role_groups:
									u_role_groups.append(g2)
						else:
							if g not in u_role_groups: 
								u_role_groups.append(g)
					break

		user, created = User.objects.get_or_create(username=u_key)
		if created:
			user.set_password(users_default_password)
			user.is_staff=r_is_staff[0]
			user.save()

		g_tmp =[]
		for u_group in u_role_groups:
			g = list([k for k in role_groups if u_group in k][0].values())[0]
			g = Group.objects.get(name = g)
			user.groups.add(g) 
			g_tmp.append(g)
		created_users_and_roles.append({u_key:g_tmp})
	return created_users_and_roles


def initialazie_base_content():
	# check if defaut database was load
	init_django_commands()

	is_dbs_available = check_dbs_available()
	if [d for d in is_dbs_available if 'default' in d][0].get('default', False):
		is_default_groups_exists_or_create = check_default_groups_exists_or_create()
		is_default_user_roles_exists_or_create = create_default_user_roles_exists_or_create()

	logger.debug(f'is_dbs_available: {is_dbs_available}')
	logger.debug(f'is_default_groups_exists_or_create: {is_default_groups_exists_or_create}')
	logger.debug(f'is_default_user_roles_exists_or_create: {is_default_user_roles_exists_or_create}')
