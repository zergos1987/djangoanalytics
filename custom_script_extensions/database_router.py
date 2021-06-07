class CheckerRouter(object):

	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'app_zs_examples' and model._meta.db_table == 'processing_module_pipeline_user_content_history':
			return 'dash_sadko_postgres_db'
		if model._meta.app_label == 'database_oracle_sadko':
			return 'oracle_sadko_db'
		elif model._meta.app_label == 'database_sqlite_test':
			return 'test_remote_db'
		return 'default'

	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'app_zs_examples' and model._meta.db_table == 'processing_module_pipeline_user_content_history':
			return 'dash_sadko_postgres_db'
		if model._meta.app_label == 'database_oracle_sadko':
			return 'oracle_sadko_db'
		elif model._meta.app_label == 'database_sqlite_test':
			return 'test_remote_db'
		return 'default'

	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'database_oracle_sadko' or obj2._meta.app_label == 'database_oracle_sadko':
			return True
		elif 'database_oracle_sadko' not in [obj1._meta.app_label, obj2._meta.app_label]:
			return True
		elif obj1._meta.app_label == 'database_sqlite_test' or obj2._meta.app_label == 'database_sqlite_test':
			return True
		elif 'database_sqlite_test' not in [obj1._meta.app_label, obj2._meta.app_label]:
			return True
		return False

	def allow_migrate(self, db, app_label, model_name=None, **hints):
		if app_label == 'database_oracle_sadko':
			return db == 'oracle_sadko_db'
		if app_label == 'database_sqlite_test':
			return db == 'test_remote_db'
		return None





