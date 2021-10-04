from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import IntegerField
from colorfield.fields import ColorField
from jsonfield import JSONField
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Create your models here.



class container_display_mode(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'

	def __str__(self):
		return self.name



class html_lang_code(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'

	def __str__(self):
		return self.name



class meta_charset_code(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'

	def __str__(self):
		return self.name



class meta_author_description(models.Model):
	author_name = models.CharField(max_length=400)
	description = models.TextField(blank=True, null=True)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'

	def __str__(self):
		return self.author_name + ' | ' + self.description



class user_settings_locale_includes(models.Model):
	name = models.CharField(max_length=100)
	label_text = models.CharField(max_length=100)
	name_order_by = IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(230)])
	is_actual = models.BooleanField(default=True)
	href = models.CharField(max_length=800, blank=True, null=True, default="#")

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('name_order_by', )
		unique_together = ('name', 'name_order_by', )

	def __str__(self):
		return (
			self.name + ' | ' + 
			str(self.name_order_by) + ' | ' + 
			str(self.is_actual) + ' | ' +
			self.label_text)


menu_level_choices = (
	("level-menu", "level-menu"),
	("level-0", "level-0"),
	("level-1", "level-1"),
	("level-2", "level-2"),
	("level-3", "level-3"),
	("level-4", "level-4"),
	("level-5", "level-5"),
)
menu_icon_type_choices = (
	("folder", "folder"),
	("arrow", "arrow"),
)
app_name_choices = (
	("zs_admin", "zs_admin"),
	("os_dashboards", "os_dashboards"),
	("zs_dashboards", "zs_dashboards"),
	("zs_examples", "zs_examples"),
)
source_type_choices = (
	("external", "external"),
	("internal", "internal"),
)

class aside_left_menu_includes(models.Model):
	parent_name = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='for_parent_name') 
	name = models.CharField(max_length=200) 
	menu_level = models.CharField(max_length=15, choices=menu_level_choices, default='level-0')
	menu_icon_type = models.CharField(max_length=15, choices=menu_icon_type_choices, default='arrow')
	name_order_by = IntegerField(default=1, choices=[(i, i) for i in range(1, 101)])
	parent_name_order_by = IntegerField(default=1, choices=[(i, i) for i in range(1, 101)])
	url_access_via_groups = models.ManyToManyField(Group, blank=True)
	url_access_via_users = models.ManyToManyField(User, blank=True)
	render_app_name = models.CharField(max_length=70, choices=app_name_choices, null=True, blank=True, default='zs_admin')
	source_app_name = models.CharField(max_length=70, choices=app_name_choices, null=True, blank=True, default='os_dashboards')
	source_app_name_translate = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='for_render_app_name_translate', limit_choices_to={'menu_level': "level-menu"}) 
	href = models.CharField(max_length=800, blank=True, null=True, default="#")
	external_href = models.TextField(blank=True, null=True, default="#")
	source_type = models.CharField(max_length=20, choices=source_type_choices, default='external')
	level_menu_svg_icon = models.TextField(blank=True, null=True)
	is_actual = models.BooleanField(default=True)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('parent_name_order_by', 'name_order_by', '-menu_icon_type', )
		unique_together = ('name', 'parent_name', 'name_order_by', 'parent_name_order_by',)
	
	def save(self, *args, **kwargs):
		if self.menu_icon_type == 'arrow':
			self.href = '#'
			self.external_href = '#'

		if self.menu_icon_type == 'folder':
			if self.source_app_name_translate.name == 'Дашборды' and self.source_type == 'external' and 'http' not in self.href:
				self.href = 'mb'
			if not 'http' in self.external_href:
				self.external_href = self.name

		if self.parent_name:
			if self.name == str(self.parent_name.name):
				if self.is_actual:
					try:
						aside_left_menu_includes.objects.filter(
							parent_name_order_by=self.name_order_by, 
							is_actual=False).exclude(id=self.id).update(is_actual=True)
					except Exception as e:
						pass
				else:
					try:
						aside_left_menu_includes.objects.filter(
							parent_name_order_by=self.name_order_by, 
							is_actual=True).exclude(id=self.id).update(is_actual=False)
					except Exception as e:
						pass

		super(aside_left_menu_includes, self).save(*args, **kwargs)

	def __str__(self):
		return (
			#str(self.render_app_name_translate) + ' | ' + 
			str(self.parent_name_order_by) + ' | ' + 
			str(self.name_order_by) + ' | ' + 
			self.menu_level + ' | ' + 
			self.menu_icon_type + ' | ' +
			str(self.render_app_name) + ' | ' +
			#self.parent_name + ' | ' +  
			self.name)




app_name_choices = (
	("zs_admin", "zs_admin"),
	("accounts", "accounts"),
	("os_dashboards", "os_dashboards"),
	("os_surveys", "os_surveys"),
	("zs_dashboards", "zs_dashboards"),
	("zs_examples", "zs_examples"),
	("db_sadko", "db_sadko"),
	("db_sqlite_test", "db_sqlite_test"),
)
class app(models.Model):
	app_brand_name = models.CharField(max_length=400, default='DjangoAnalytics')
	app_brand_color = ColorField(default='#333')
	app_brand_ico = models.ImageField(upload_to='img', null=True)
	app_brand_logo = models.ImageField(upload_to='img', null=True)
	app_brand_logo_zoom = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(3.0)], default=1)
	app_breadcrumb_active = models.CharField(max_length=400, default='', blank=True)
	app_settings_container_display_mode = models.ManyToManyField(container_display_mode)
	app_settings_html_lang_code = models.ForeignKey(html_lang_code, on_delete=models.CASCADE, unique=False, null=True, blank=True)
	app_settings_meta_charset_code = models.ForeignKey(meta_charset_code, on_delete=models.CASCADE, null=True, blank=True)
	app_settings_meta_author_description = models.ForeignKey(meta_author_description, on_delete=models.CASCADE, null=True, blank=True)
	app_settings_header_section_left_enable = models.BooleanField(default=True)
	app_settings_header_section_left_button_menu_enable = models.BooleanField(default=True)
	app_settings_header_section_left_brand_details_enable = models.BooleanField(default=True)
	app_settings_header_section_center_enable = models.BooleanField(default=True)
	app_settings_header_section_right_enable = models.BooleanField(default=True)
	app_settings_header_section_right_search_extra_button_enable = models.BooleanField(default=True)
	app_settings_header_section_right_notification_enable = models.BooleanField(default=True)
	app_settings_header_section_right_user_settings_enable = models.BooleanField(default=True)
	app_settings_header_section_right_user_settings_locale_enable = models.BooleanField(default=True)
	app_settings_header_section_right_user_settings_locale_includes = models.ManyToManyField(user_settings_locale_includes, blank=True,  limit_choices_to = {'is_actual': True})
	app_settings_header_section_right_user_settings_menu_enable = models.BooleanField(default=True)
	app_settings_container_aside_left_enable = models.BooleanField(default=True)
	app_settings_container_aside_left_main_site_page = models.CharField(max_length=70, choices=app_name_choices, null=True, blank=True) 
	app_start_page = models.CharField(max_length=70, choices=app_name_choices, null=True, blank=False, default='zs_admin') 
	app_settings_container_aside_left_menu_items_includes = models.ManyToManyField(aside_left_menu_includes, related_name='aside_left_menu', blank=True,  limit_choices_to = {'is_actual': True})
	app_settings_container_main_bg_color_enable = models.BooleanField(default=True)
	app_settings_container_main_bg_color = ColorField(default='#f9f9f9')
	app_settings = JSONField(default=list, null=True, blank=True)
	is_actual = models.BooleanField(default=False)

	class Meta:
		app_label = 'app_zs_admin'
		unique_together = ('app_brand_name', 'app_brand_ico', 'app_brand_logo', 'app_breadcrumb_active')

	def save(self, *args, **kwargs):
		if self.is_actual:
			try:
				app.objects.filter(is_actual=True).exclude(id=self.id).update(is_actual=False)
			except Exception as e:
				pass
		super(app, self).save(*args, **kwargs)

	def __str__(self):
		field_values = []
		for field in self._meta.get_fields():
			field_values.append(str(getattr(self, field.name, '')))
		field_values = ['app_brand_name', 'is_actual',]
		return ' '.join(field_values)



class notification_events(models.Model):
	title = models.CharField(max_length=400)
	event_date = models.DateTimeField(auto_now_add=True, blank=False)
	event_content = models.CharField(max_length=100, blank=True, null=True)
	event_content2 = RichTextField(config_name='default', blank=True, null=True)
	users_list = models.ManyToManyField(User, related_name='for_user_notification_event_show', blank=True)
	is_actual = models.BooleanField(default=False)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('-event_date', )

	def __str__(self):
		return (
			str(self.title) + ' | ' + 
			str(self.event_date) + ' | ' + 
			str(self.event_content) + ' | ' +
			str(self.is_actual))



class user_notification_event_confirm(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="for_user_notification_event_confirm")
	confirm_date = models.DateTimeField(auto_now_add=True, blank=False)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('-confirm_date', 'user' )

	def save(self, *args, **kwargs):
		self.confirm_date = timezone.now()
		super(user_notification_event_confirm, self).save(*args, **kwargs)

	def __str__(self):
		return (
			str(self.user) + ' | ' + 
			str(self.confirm_date))



update_week_days_list_choices = (
		('monday', 'monday'),
		('tuesday', 'tuesday'),
		('wednesday', 'wednesday'),
		('thursday', 'thursday'),
		('friday', 'friday'),
	)
class week_intervals(models.Model):
	update_week_days_list = models.CharField(max_length=70, choices=update_week_days_list_choices, null=False, blank=False) 
	is_actual = models.BooleanField(default=True) 

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('is_actual',)
		unique_together = ('update_week_days_list', )

	def __str__(self):
		return (
			str(self.update_week_days_list))



update_time_list_choices = ()
for j in [i for i in range(0, 24)]:
	for i in [':00', ':05', ':10', ':15', ':20', ':25', ':30', ':35', ':40', ':45', ':50', ':55']:
		j = str(j)
		if len(str(j)) < 2: j = '0' + j
		update_time_list_choices = update_time_list_choices + ((j + i, j + i),)

class time_intervals(models.Model):
	update_time_list = models.CharField(max_length=70, choices=update_time_list_choices, null=False, blank=False)
	is_actual = models.BooleanField(default=True) 

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('is_actual',)
		unique_together = ('update_time_list', )

	def __str__(self):
		return (
			str(self.update_time_list))



database_names_list_choices = (
		('khd', 'khd'),
		('sadko', 'sadko'),
		('djangoanalytics', 'djangoanalytics'),
	)
database_schemas_list_choices = (
		('dak', 'dak'),
		('djangoanalytics', 'djangoanalytics'),
		('djangoanalytics_dashboards', 'djangoanalytics_dashboards'),
	)
class etl_job_database_tables_tasks(models.Model):
	limit_rows = models.IntegerField(null=False, blank=False, default=30000, validators=[MinValueValidator(1), MaxValueValidator(100000)])
	update_week_days_list = models.ManyToManyField(week_intervals, blank=True, limit_choices_to = {'is_actual': True})
	update_time_list = models.ManyToManyField(time_intervals, blank=True, limit_choices_to = {'is_actual': True}) 
	database_name_from = models.CharField(max_length=200, choices=database_names_list_choices, null=False, blank=False)
	database_name_to = models.CharField(max_length=200, choices=database_names_list_choices, null=False, blank=False)
	table_schema_from = models.CharField(max_length=200, choices=database_schemas_list_choices, null=False, blank=False)
	table_schema_to = models.CharField(max_length=200, choices=database_schemas_list_choices, null=False, blank=False)
	table_name_prefix = models.CharField(max_length=200, null=True, blank=True, default='xxx')
	table_name_from = models.CharField(max_length=300, null=False, blank=False)
	create_table_if_not_exists = models.BooleanField(default=True)
	where_condition_from = models.TextField(blank=True, null=True)
	where_condition_to = models.TextField(blank=True, null=True)
	columns_from = models.TextField(null=False, blank=False, default='*')
	columns_for_unique_id = models.TextField(null=False, blank=False, default='*')
	clear_all_data_before_insert = models.BooleanField(default=True)
	remove_duplicates_table_to = models.BooleanField(default=False)
	update_exists_rows = models.BooleanField(default=False)
	insert_only_new_rows = models.BooleanField(default=False) 
	insert_all_rows = models.BooleanField(default=True)
	drop_table_to = models.BooleanField(default=False)
	steps_delay_seconds = models.IntegerField(null=False, blank=False, default=5, validators=[MinValueValidator(2), MaxValueValidator(30)])
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="for_etl_job_database_tables_tasks_created_by")
	created_date = models.DateTimeField(auto_now_add=True, blank=False)
	updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="for_etl_job_database_tables_tasks_updated_by")
	updated_date = models.DateTimeField(auto_now=True, blank=False)
	etl_error_flag = models.BooleanField(default=False)
	is_actual = models.BooleanField(default=False)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('is_actual', '-created_by',)

	def save(self, *args, **kwargs):
		#self.table_name_prefix = self.database_name_from
		super(etl_job_database_tables_tasks, self).save(*args, **kwargs)

	def __str__(self):
		return (
			str(self.database_name_from) + ' | ' + 
			str(self.table_schema_from) + ' | ' + 
			str(self.table_name_prefix) + ' | ' + 
			str(self.table_name_from) + ' | ' + 
			str(self.is_actual))


class etl_job_database_tables_tasks_logs(models.Model):
	etl_job_database_tables_tasks_fk = models.ForeignKey(etl_job_database_tables_tasks, on_delete=models.CASCADE, unique=False, null=True, blank=True, related_name="for_etl_job_database_tables_tasks_logs")
	table_rows_count = models.IntegerField(null=False, blank=False, default=0, validators=[MinValueValidator(0)])
	error_message = models.TextField(null=True, blank=True, default='')
	updated_at = models.DateTimeField(auto_now_add=True, blank=False)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('-updated_at',)

	def save(self, *args, **kwargs):
		super(etl_job_database_tables_tasks_logs, self).save(*args, **kwargs)

	def __str__(self):
		if self.etl_job_database_tables_tasks_fk.table_name_prefix:
			table_name_prefix = self.etl_job_database_tables_tasks_fk.table_name_prefix + '_'
		else:
			table_name_prefix = ''
		if self.updated_at:
			updated_at = self.updated_at.strftime("%m.%d.%Y, %H:%M:%S")
		else:
			updated_at = self.updated_at

		if self.error_message:
			if len(self.error_message) > 0: error_message = 1
		else:
			error_message = 0

		to_ = (
			'[TO]: ' +
			self.etl_job_database_tables_tasks_fk.database_name_to + '.' +
			self.etl_job_database_tables_tasks_fk.table_schema_to + '.' +
			table_name_prefix +
			self.etl_job_database_tables_tasks_fk.table_name_from
			)
		from_ = (
			'[FROM]: ' +
			self.etl_job_database_tables_tasks_fk.database_name_from + '.' +
			self.etl_job_database_tables_tasks_fk.table_schema_from + '.' +
			self.etl_job_database_tables_tasks_fk.table_name_from
			)
		return (
			'[HAVE ERRORS]: ' + str(error_message) + ' ' +
			'[DATE]: ' + updated_at + ' ' +
			' [ID]: ' + str(self.etl_job_database_tables_tasks_fk.id) + ' ' +
			from_ + 
			' >>> ' + 
			to_ + ' ' + 
			' [ROWS]: ' + str(self.table_rows_count)
			)
