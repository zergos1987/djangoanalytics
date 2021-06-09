# from django.db import connections
# from django.db.utils import OperationalError



def check_default_db_available():
	# db_conn = connections['default']

	# try:
	# 	c = db_conn.cursor()
	# except OperationalError:
	# 	connected = False
	# else:
	# 	connected = True

	return True


def check_default_groups_exists():
	return True, ['a', 'b']


def initialazie_base_content():
	# check if defaut database was load
	is_default_db_available = check_default_db_available()
	if is_default_db_available:
		is_default_groups_exists, group_list = check_default_groups_exists()


	print('\ndjangoanalytics_initialize.py script output:')
	print('   is_default_db_available:', is_default_db_available)
	print('   is_default_groups_exists:', is_default_db_available, 'group_list:', group_list)
