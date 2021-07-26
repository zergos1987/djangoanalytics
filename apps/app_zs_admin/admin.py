from django.contrib import admin
from django.contrib import messages, admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
	app,
        container_display_mode,
        html_lang_code,
        meta_charset_code,
        meta_author_description,
        user_settings_locale_includes,
        aside_left_menu_includes,
	)

# Register your models here.
class appResource(resources.ModelResource):

    class Meta:
        model = app
        fields = (
            'app_brand_name','app_brand_color', 'app_brand_ico', 'app_brand_logo', 'is_actual',)

class appAdmin(ImportExportModelAdmin):
    list_display = [
    	'id', 'app_brand_name', 'app_brand_color', 'app_brand_ico', 'app_brand_logo', 'is_actual']

    list_filter = (
        'app_brand_name', 'is_actual',  #('dt', DateTimeRangeFilter)
    )

    filter_horizontal = (
        'app_settings_container_display_mode', 
        'app_settings_header_section_right_user_settings_locale_includes',
        'app_settings_container_aside_left_menu_items_includes',)
    
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

    # class Media:
    #     js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = appResource
admin.site.register(app, appAdmin)



class container_display_modeResource(resources.ModelResource):
    class Meta:
        model = container_display_mode
        fields = (
            'name',)

class container_display_modeAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'name']

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

    # class Media:
    #     js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = container_display_modeResource
admin.site.register(container_display_mode, container_display_modeAdmin)



class html_lang_codeResource(resources.ModelResource):
    class Meta:
        model = html_lang_code
        fields = (
            'name',)

class html_lang_codeAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'name']

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

    # class Media:
    #     js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = html_lang_codeResource
admin.site.register(html_lang_code, html_lang_codeAdmin)



class meta_charset_codeResource(resources.ModelResource):
    class Meta:
        model = meta_charset_code
        fields = (
            'name',)

class meta_charset_codeAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'name']

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

    # class Media:
    #     js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = meta_charset_codeResource
admin.site.register(meta_charset_code, meta_charset_codeAdmin)



class meta_author_descriptionResource(resources.ModelResource):
    class Meta:
        model = meta_author_description
        fields = (
            'author_name', 'description',)

class meta_author_descriptionAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'author_name', 'description']

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

    # class Media:
    #     js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = meta_author_descriptionResource
admin.site.register(meta_author_description, meta_author_descriptionAdmin)



class user_settings_locale_includesResource(resources.ModelResource):
    class Meta:
        model = user_settings_locale_includes
        fields = (
            'name', 'label_text', 'name_order_by', 'is_actual', 'href',)

class user_settings_locale_includesAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'name', 'label_text', 'name_order_by', 'is_actual', 'href']

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

    # class Media:
    #     js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = user_settings_locale_includesResource
admin.site.register(user_settings_locale_includes, user_settings_locale_includesAdmin)



class aside_left_menu_includesResource(resources.ModelResource):
    class Meta:
        model = aside_left_menu_includes
        fields = (
            'name',  'menu_level', 'menu_icon_type',  'parent_name_order_by', 'name_order_by', 'render_app_name', 'source_app_name_translate', 'href', 'is_actual', ) 

class aside_left_menu_includesAdmin(ImportExportModelAdmin):
    list_display = [
        'id', 'parent_name_short', 'name',  'menu_level', 'menu_icon_type', 'parent_name_order_by', 'name_order_by', 'render_app_name', 'get_source_app_name_translate_name', 'href', 'is_actual']

    list_filter = (
        'name',  'is_actual',  #('dt', DateTimeRangeFilter)
    )

    def get_source_app_name_translate_name(self, obj):
        if obj.source_app_name_translate:
            return obj.source_app_name_translate.name
        else:
            '--'
    get_source_app_name_translate_name.short_description = 'menu_level_name'
    get_source_app_name_translate_name.admin_order_field = 'source_app_name_translate__name'

    filter_horizontal = ('url_access_via_groups', 'url_access_via_users',)
    def parent_name_short(self, obj):
        if obj.name:
            if obj.parent_name:
                return obj.parent_name.name

    def save_model(self, request, obj, form, change):
        if obj.menu_icon_type == "arrow" and obj.href != '#':
            messages.error(request, "Cannot save menu_icon_type = arrow and href != '#'. Change menu_icon_type for saving href !")
        super(aside_left_menu_includesAdmin, self).save_model(request, obj, form, change)

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

    # class Media:
    #     js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = aside_left_menu_includesResource
admin.site.register(aside_left_menu_includes, aside_left_menu_includesAdmin)
