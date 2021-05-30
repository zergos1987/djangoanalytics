class CheckerRouter(object):

	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'examples' and model._meta.db_table == 'processing_module_pipeline_user_content_history':
			return 'dash_sadko_postgres_db'

		elif model._meta.app_label == 'examples':
			return 'test_sqlite3_db'

		elif model._meta.app_label == 'op_dashboards':
			return 'op_dashboards_sqlite3_db'

		elif model._meta.app_label == 'op_surveys':
			return 'op_surveys_sqlite3_db'

		return 'default'



	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'examples' and model._meta.db_table == 'processing_module_pipeline_user_content_history':
			return 'dash_sadko_postgres_db'

		elif model._meta.app_label == 'examples':
			return 'test_sqlite3_db'

		elif model._meta.app_label == 'op_dashboards':
			return 'op_dashboards_sqlite3_db'

		elif model._meta.app_label == 'op_surveys':
			return 'op_surveys_sqlite3_db'

		return 'default'



	def allow_relation(self, obj1, obj2, **hints):
		if obj1._meta.app_label == 'dash_sadko' or obj2._meta.app_label == 'dash_sadko':
			return True
		elif 'dash_sadko' not in [obj1._meta.app_label, obj2._meta.app_label]:
			return True

		elif obj1._meta.app_label == 'examples' or obj2._meta.app_label == 'examples':
			return True
		elif 'examples' not in [obj1._meta.app_label, obj2._meta.app_label]:
			return True

		elif obj1._meta.app_label == 'op_dashboards' or obj2._meta.app_label == 'op_dashboards':
			return True
		elif 'op_dashboards' not in [obj1._meta.app_label, obj2._meta.app_label]:
			return True

		elif obj1._meta.app_label == 'op_surveys' or obj2._meta.app_label == 'op_surveys':
			return True
		elif 'op_surveys' not in [obj1._meta.app_label, obj2._meta.app_label]:
			return True

		return False



	def allow_migrate(self, db, app_label, model_name=None, **hints):
		if app_label == 'examples':
			return db == 'test_sqlite3_db'

		if app_label == 'op_dashboards':
			return db == 'op_dashboards_sqlite3_db'

		if app_label == 'op_surveys':
			return db == 'op_surveys_sqlite3_db'

		return None







