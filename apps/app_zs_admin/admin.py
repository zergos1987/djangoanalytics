from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
		app,
        container_display_mode,
        html_lang_code,
        meta_charset_code,
        meta_author_description,
        user_settings_locale_includes,
        settings_menu_includes,
	)

# Register your models here.
class appResource(resources.ModelResource):

    class Meta:
        model = app
        fields = (
            'app_brand_name','app_brand_color', 'app_brand_ico', 'app_brand_logo', 'is_actual',)

class appAdmin(ImportExportModelAdmin):
    list_display = [
    	'app_brand_name', 'app_brand_color', 'app_brand_ico', 'app_brand_logo', 'is_actual']

    list_filter = (
        'app_brand_name', 'is_actual',  #('dt', DateTimeRangeFilter)
    )
    
    def has_import_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_export_permission(self, request, obj=None):
        return True
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = appResource
admin.site.register(app, appAdmin)



class container_display_modeResource(resources.ModelResource):
    class Meta:
        model = container_display_mode
        fields = (
            'name',)

class container_display_modeAdmin(ImportExportModelAdmin):
    list_display = [
        'name']

    list_filter = (
        'name',  #('dt', DateTimeRangeFilter)
    )
    
    def has_import_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_export_permission(self, request, obj=None):
        return True
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = container_display_modeResource
admin.site.register(container_display_mode, container_display_modeAdmin)



class html_lang_codeResource(resources.ModelResource):
    class Meta:
        model = html_lang_code
        fields = (
            'name',)

class html_lang_codeAdmin(ImportExportModelAdmin):
    list_display = [
        'name']

    list_filter = (
        'name',  #('dt', DateTimeRangeFilter)
    )
    
    def has_import_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_export_permission(self, request, obj=None):
        return True
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = html_lang_codeResource
admin.site.register(html_lang_code, html_lang_codeAdmin)



class meta_charset_codeResource(resources.ModelResource):
    class Meta:
        model = meta_charset_code
        fields = (
            'name',)

class meta_charset_codeAdmin(ImportExportModelAdmin):
    list_display = [
        'name']

    list_filter = (
        'name',  #('dt', DateTimeRangeFilter)
    )
    
    def has_import_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_export_permission(self, request, obj=None):
        return True
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = meta_charset_codeResource
admin.site.register(meta_charset_code, meta_charset_codeAdmin)



class meta_author_descriptionResource(resources.ModelResource):
    class Meta:
        model = meta_author_description
        fields = (
            'author_name', 'description',)

class meta_author_descriptionAdmin(ImportExportModelAdmin):
    list_display = [
        'author_name', 'description']

    list_filter = (
        'author_name',  #('dt', DateTimeRangeFilter)
    )
    
    def has_import_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_export_permission(self, request, obj=None):
        return True
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = meta_author_descriptionResource
admin.site.register(meta_author_description, meta_author_descriptionAdmin)



class user_settings_locale_includesResource(resources.ModelResource):
    class Meta:
        model = user_settings_locale_includes
        fields = (
            'name', 'label_text', 'name_order_by', 'is_actual', 'href',)

class user_settings_locale_includesAdmin(ImportExportModelAdmin):
    list_display = [
        'name', 'label_text', 'name_order_by', 'is_actual', 'href']

    list_filter = (
        'name', 'is_actual',  #('dt', DateTimeRangeFilter)
    )
    
    def has_import_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_export_permission(self, request, obj=None):
        return True
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = user_settings_locale_includesResource
admin.site.register(user_settings_locale_includes, user_settings_locale_includesAdmin)



class settings_menu_includesResource(resources.ModelResource):
    class Meta:
        model = user_settings_locale_includes
        fields = (
            'name', 'parent_name', 'menu_level', 'menu_icon_type', 'name_order_by', 'parent_name_order_by', 'is_actual',  'href',  ) 

class settings_menu_includesAdmin(ImportExportModelAdmin):
    list_display = [
        'name', 'parent_name', 'menu_level', 'menu_icon_type', 'name_order_by', 'parent_name_order_by', 'is_actual',  'href']

    list_filter = (
        'name', 'parent_name',  'is_actual',  #('dt', DateTimeRangeFilter)
    )
    
    def has_import_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_export_permission(self, request, obj=None):
        return True
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return False

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = settings_menu_includesResource
admin.site.register(settings_menu_includes, settings_menu_includesAdmin)