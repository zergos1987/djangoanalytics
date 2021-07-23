from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import IntegerField
from colorfield.fields import ColorField
from jsonfield import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator



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
render_app_name_translate = (
	("Приложения", "Приложения"),
	("Дашборды", "Дашборды"),
)
source_type_choices = (
	("external", "external"),
	("internal", "internal"),
)
class aside_left_menu_includes(models.Model):
	parent_name = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True) 
	name = models.CharField(max_length=200) 
	menu_level = models.CharField(max_length=15, choices=menu_level_choices, default='level-0')
	menu_icon_type = models.CharField(max_length=15, choices=menu_icon_type_choices, default='arrow')
	name_order_by = IntegerField(default=1, choices=[(i, i) for i in range(1, 101)])
	parent_name_order_by = IntegerField(default=1, choices=[(i, i) for i in range(1, 101)])
	url_access_via_groups = models.ManyToManyField(Group, blank=True)
	url_access_via_users = models.ManyToManyField(User, blank=True)
	render_app_name  = models.CharField(max_length=70, choices=app_name_choices, null=True, blank=True)
	render_app_name_translate = models.CharField(max_length=150, choices=render_app_name_translate, null=False, default='Дашборды')
	is_new_parent_menu = models.BooleanField(default=False)
	href = models.CharField(max_length=800, blank=True, null=True, default="#")
	content_href = models.TextField(blank=True, null=True, default="#")
	source_type = models.CharField(max_length=20, choices=source_type_choices, default='external')
	level_menu_svg_icon = models.TextField(blank=True, null=True)
	is_actual = models.BooleanField(default=True)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		ordering = ('parent_name_order_by', 'name_order_by', )
		unique_together = ('name', 'parent_name', 'name_order_by', 'parent_name_order_by',)
	
	def save(self, *args, **kwargs):
		if self.menu_icon_type == 'arrow' and self.href != '#':
			self.href = '#'

		if self.parent_name:
			if self.name == str(self.parent_name):
				if self.is_actual:
					try:
						aside_left_menu_includes.objects.filter(
							name_order_by=self.name_order_by, 
							is_actual=False).exclude(id=self.id).update(is_actual=True)
					except Exception as e:
						pass
				else:
					try:
						aside_left_menu_includes.objects.filter(
							name_order_by=self.name_order_by, 
							is_actual=True).exclude(id=self.id).update(is_actual=False)
					except Exception as e:
						pass

		super(aside_left_menu_includes, self).save(*args, **kwargs)

	def __str__(self):
		return (
			self.render_app_name_translate + ' | ' + 
			str(self.parent_name_order_by) + ' | ' + 
			str(self.name_order_by) + ' | ' + 
			self.menu_level + ' | ' + 
			self.menu_icon_type + ' | ' +
			str(self.is_new_parent_menu) + ' | ' +
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
	app_settings_container_aside_left_settings_menu_enable = models.BooleanField(default=True)
	app_settings_container_aside_left_settings_menu_items_includes = models.ManyToManyField(aside_left_menu_includes, related_name='settings_menu', blank=True,  limit_choices_to = {'is_actual': True})
	app_settings_container_aside_left_dashboards_menu_enable = models.BooleanField(default=True)
	app_settings_container_aside_left_dashboards_menu_items_includes = models.ManyToManyField(aside_left_menu_includes, related_name='dashboards_menu', blank=True,  limit_choices_to = {'is_actual': True})
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
