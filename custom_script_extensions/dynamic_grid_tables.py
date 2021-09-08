from apps.accounts.models import user_extra_details
from apps.app_zs_admin.models import app, aside_left_menu_includes
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType 


from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import FloatField, CharField
from django.db.models.functions import Cast
from django.db.models import Max, Case, Value, When
from django.db.models import Aggregate, CharField, Value
import re



def get_table_settings(table_name, url_for_render, request):
	settings = {}
	settings['table_name'] = table_name

	request_table_secure_values_hide_FOR_ALL = [
		"app_opensource_dashboards_viewer_group",
		"app_zs_dashboards_viewer_group",
		"Новая запись",
	]
	fathgrid_initialize_settings_FOR_ALL = {
		'grid_properties': {
			'base_properties': """
				size: 10, 
				page: 1, 
				pageNumberBase: 0,
				editable: true,
				filterable: true,
				sortable: true,
				printable: true,
				resizable: false,
				restoreColumns: true,
				pageable: false,
				exportable: true,
				showGraph: true,
				showFooter: true,
				selectColumns: true,
				showGrouping: true,
				showTableTotal: true,
				showGroupHeader: true,
				showGroupFooter: true,
				showGroupRows: true,
			""",
			'serverURL': f"""{request.build_absolute_uri('/')[:-1]}{url_for_render}""",
		},
		'columns_properties': """""",
		'columns_settings': {
			'listOfValues': {
				'parent_name__name': ['name'],
				'menu_level': ['menu_level'],
				'menu_icon_type': ['menu_icon_type'],
				'url_access_via_groups': [],
			}
		}
	}



	if settings['table_name'] == 'aside_left_menu_includes':
		settings['request_table_title'] = 'Настройки доступа и ссылки'
		settings['fathgrid_initialize_settings'] = fathgrid_initialize_settings_FOR_ALL
		settings['request_table_columns_id'] = 'id'
		settings['request_table_max_limit_rows'] = 5000
		settings['request_table_as_dict'] = False
		settings['request_m2m_join_columns'] = ['url_access_via_groups__name', 'url_access_via_users__username']
		settings['get_media'] = True
		settings['request_table_columns_props'] = [
			{
				'db_name': 'id', 
				'grid_header_name': 'id',
				'grid_column_props': {
					'label': '',
					'class': 'text-center',
					'disabled': 'true',
					'pattern': '[0-9]{1,10}',
					'editable': 'false',
					'filterable': 'true',
					'type': '',
					'listOfValues': [],
					'footer': '`Итого (уникальные):`',
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'parent_name__name', 
				'grid_header_name': 'Меню: контент, принадлежность',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'true',
					'filterable': 'true',
					'type': '',
					'listOfValues': ['Дашборды','ЦИРКП'],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'name', 
				'grid_header_name': 'Контент',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'true',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'menu_level', 
				'grid_header_name': 'Меню: контент, уровень вложения', 
				'grid_column_props': {
					'label': '',
					'class': 'text-center',
					'disabled': 'false',
					'pattern': '',
					'editable': 'true',
					'filterable': 'true',
					'type': '',
					'listOfValues': ['level-1','level-2','level-3','level-4','level-5'],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'menu_icon_type', 
				'grid_header_name': 'Меню: контент, тип вложения',
				'grid_column_props': {
					'label': '',
					'class': 'text-center',
					'disabled': 'false',
					'pattern': '',
					'editable': 'true',
					'filterable': 'true',
					'type': '',
					'listOfValues': ['arrow','folder'],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'name_order_by', 
				'grid_header_name': 'Меню: контент, порядок расположения',
				'grid_column_props': {
					'label': '',
					'class': 'text-center',
					'disabled': 'false',
					'pattern': '[0-9]*',
					'editable': 'true',
					'filterable': 'true',
					'type': 'number',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'url_access_via_groups__name', 
				'grid_header_name': 'Доступ к ресурсу: группы',
				'grid_column_props': {
					'label': '',
					'class': 'text-left',
					'disabled': 'false',
					'pattern': '',
					'editable': 'true',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'url_access_via_users__username',
				'grid_header_name': 'Доступ к ресурсу: пользователи',
				'grid_column_props': {
					'label': '',
					'class': 'text-left',
					'disabled': 'false',
					'pattern': '',
					'editable': 'true',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}
		]
		settings['request_table_filters'] = [
			("source_app_name_translate__name", "exact",  "Дашборды"),
			("is_actual", "",  True),
			# ("source_app_name_translate__name", "not_equal",  "fff"),
			# ("source_app_name_translate__name", "starts_with",  "aaa"),
			# ("source_app_name_translate__name", "equal",  100)
		]
		settings['request_table_excludes'] = [
			("name", "exact",  "Дашборды"),
		]
		settings['request_table_secure_values_hide'] = [
		] + request_table_secure_values_hide_FOR_ALL
		settings['add_row_default'] = {
			'parent_name': aside_left_menu_includes.objects.filter(name__exact='Дашборды').first(),
			'source_app_name_translate': aside_left_menu_includes.objects.filter(name__exact='Дашборды').first(), 
			'parent_name_order_by': aside_left_menu_includes.objects.filter(name__exact='Дашборды').first().parent_name_order_by,
			'name_order_by': aside_left_menu_includes.objects.filter(source_app_name_translate__name__exact='Дашборды').aggregate(Max('name_order_by')).get('name_order_by__max', 1)+1,
			'name': 'Новая запись',
			'menu_level': 'level-1',
			'menu_icon_type': 'folder',
			'render_app_name': 'zs_admin',
			'source_app_name': 'os_dashboards',
			'href': 'mb',
			'external_href': 'Новая запись',
			'source_type': 'external',
			'url_access_via_groups': Group.objects.filter(name__in=['app_opensource_dashboards_viewer_group', 'app_zs_dashboards_viewer_group']),
		}



	if settings['table_name'] == 'user_extra_details':
		settings['request_table_title'] = 'Пользователи'
		settings['fathgrid_initialize_settings'] = fathgrid_initialize_settings_FOR_ALL
		settings['request_table_columns_id'] = None
		settings['request_table_max_limit_rows'] = 5000
		settings['request_table_as_dict'] = True
		settings['request_m2m_join_columns'] = []
		settings['get_media'] = False
		settings['request_table_columns_props'] = [
			{
				'db_name': 'id', 
				'grid_header_name': 'id',
				'grid_column_props': {
					'label': '',
					'class': 'text-center',
					'disabled': 'true',
					'pattern': '[0-9]{1,10}',
					'editable': 'false',
					'filterable': 'true',
					'type': '',
					'listOfValues': [],
					'footer': '`Итого (уникальные):`',
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'user__username', 
				'grid_header_name': 'user_id',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'false',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'full_name', 
				'grid_header_name': 'ФИО',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'false',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'department', 
				'grid_header_name': 'Департамент',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'false',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'center', 
				'grid_header_name': 'Центр',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'false',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'position', 
				'grid_header_name': 'Должность',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'false',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}
		]
		settings['request_table_filters'] = [
			("user__is_active", "",  True),
			("ldap_is_active", "",  True),
		]
		settings['request_table_excludes'] = [
			# ("user__is_superuser", "",  True),
			# ("user__is_staff", "",  True),
		]
		settings['request_table_secure_values_hide'] = [
		] + request_table_secure_values_hide_FOR_ALL
		settings['add_row_default'] = {}


	if settings['table_name'] == 'group':
		settings['request_table_title'] = 'Группы'
		settings['fathgrid_initialize_settings'] = fathgrid_initialize_settings_FOR_ALL
		settings['request_table_columns_id'] = 'id'#None
		settings['request_table_max_limit_rows'] = 5000
		settings['request_table_as_dict'] = True
		settings['request_m2m_join_columns'] = []
		settings['get_media'] = False
		settings['request_table_columns_props'] = [
			{
				'db_name': 'id', 
				'grid_header_name': 'id',
				'grid_column_props': {
					'label': '',
					'class': 'text-center',
					'disabled': 'true',
					'pattern': '[0-9]{1,10}',
					'editable': 'false',
					'filterable': 'true',
					'type': '',
					'listOfValues': [],
					'footer': '`Итого (уникальные):`',
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}, {
				'db_name': 'name', 
				'grid_header_name': 'Группы',
				'grid_column_props': {
					'label': '',
					'class': '',
					'disabled': 'false',
					'pattern': '',
					'editable': 'true',
					'filterable': 'true',
					'type': 'textarea',
					'listOfValues': [],
					'footer': """(data,el) => `${data.map(item => item.$$$COLUMN$$$).filter((value, index, self) => self.indexOf(value) === index).length}`""",
					'html': """x => `<div class="table-tbody-td-div"><div>${RenderRow(x.$$$COLUMN$$$, false)}</div></div>`"""
				}
			}
		]
		settings['request_table_filters'] = [
			("name", "startswith",  'SADKO'),
		]
		settings['request_table_excludes'] = [
		]
		settings['request_table_secure_values_hide'] = [
		] + request_table_secure_values_hide_FOR_ALL
		settings['add_row_default'] = {
			'name': 'SADKO_новая_группа',
		}

	return settings 
