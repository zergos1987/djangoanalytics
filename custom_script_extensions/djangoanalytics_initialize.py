from django.core.management import call_command
from django.db import connections
from django.contrib.auth.models import User, Group
import logging

logger = logging.getLogger(__name__)

database_names = [
	'default', 
	'dash_sadko_postgres_db'
]
role_groups = [
	{1: 'accounts'}, 
	{2: 'app_opensource_dashboards'}, 
	{3: 'app_opensource_surveys'},
	{4: 'app_zs_admin'},
	{5: 'app_zs_dashboards'},
	{6: 'app_zs_examples'},
	{7: 'database_oracle_sadko'},
	{8: 'database_sqlite_test'},
	{60001: 'app_zs_examples__genericTable__drf__get'},
	{60002: 'app_zs_examples__genericTable__drf__post'},
	{60003: 'app_zs_examples__genericTable__drf__put'},
	{60004: 'app_zs_examples__genericTable__drf__delete'},
	{60005: 'app_zs_examples__genericTable__drf__export'},
	{60006: 'app_zs_examples__genericTable__drf__import'},
	{60007: 'app_zs_examples__test_table_model__drf__get'},
	{60008: 'app_zs_examples__test_table_model__drf__post'},
	{60009: 'app_zs_examples__test_table_model__drf__put'},
	{60010: 'app_zs_examples__test_table_model__drf__delete'},
	{60011: 'app_zs_examples__test_table_model__drf__export'},
	{60012: 'app_zs_examples__test_table_model__drf__import'},
]
user_roles = [
	{
		'admin_ROLE': {
			'user_groups': [
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
		'accounts_ROLE': {
			'user_groups': [1], 
			'is_staff': [False]
		}
	},{
		'app_opensource_dashboards_ROLE': {
			'user_groups': [2], 
			'is_staff': [False]
		}
	},{
		'app_opensource_surveys_ROLE': {
			'user_groups': [3], 
			'is_staff': [False]
		}
	},{
		'app_zs_admin_ROLE': {
			'user_groups': [4], 
			'is_staff': [False]
		}
	},{
		'app_zs_dashboards_ROLE': {
			'user_groups': [5], 
			'is_staff': [False]
		}
	},{
		'app_zs_examples_ROLE': {
			'user_groups': [6, 60001, 60002, 60003, 60004, 60005, 60006, 60007, 60008, 60009, 60009, 60010, 60011, 60012], 
			'is_staff': [False]
		}
	},{
		'database_oracle_sadko_ROLE': {
			'user_groups': [7], 
			'is_staff': [False]
		}
	},{
		'database_sqlite_test_ROLE': {
			'user_groups': [8], 
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
		'api_user': {
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
