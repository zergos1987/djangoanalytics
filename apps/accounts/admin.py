from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.auth.models import Permission

from .models import (
    app,
	AuditEntry,
    UserSession
	)


# Register your models here.
admin.site.register(Permission)

class appResource(resources.ModelResource):

    class Meta:
        model = app
        fields = (
            'test_field',)


class appAdmin(ImportExportModelAdmin):
    list_display = [
        'test_field',]

    list_filter = (
        'test_field',  #('dt', DateTimeRangeFilter)
    )

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = appResource
admin.site.register(app, appAdmin)



class AuditEntryResource(resources.ModelResource):

    class Meta:
        model = AuditEntry
        fields = (
            'dt', 
            'action', 
            'request_method', 
            'username', 
            'ip', 
            'device', 
            'browser_family', 
            'browser_version', 
            'os_family', 
            'os_version',)

	
class AuditEntryAdmin(ImportExportModelAdmin):
    list_display = [
    	'dt', 
    	'action', 
    	'request_method', 
    	'username', 
    	'ip', 
    	'device', 
    	'browser_family', 
    	'browser_version', 
    	'os_family', 
    	'os_version',]

    list_filter = (
        'dt', 'action', #('dt', DateTimeRangeFilter)
    )

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = AuditEntryResource
admin.site.register(AuditEntry, AuditEntryAdmin)



class CustomUserAdmin(UserAdmin):
    class Media:
        js = ['/apps/accounts/origin/js/custom_admin_script.js', '/static/admin/js/jquery.grp_timepicker.js']
        css = {
            'all': ('apps/accounts/origin/css/custom_admin_style.css',)
        }   
        #js = ['apps/accounts/origin/js/custom_admin_script.js']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



class UserSessionResource(resources.ModelResource):

    class Meta:
        model = UserSession
        fields = (
            'user', 
            'session',)

class UserSessionAdmin(ImportExportModelAdmin):
    list_display = [
        'user', 
        'session', 'created_at', 'remove_session']

    list_filter = (
        'user', 'session', 'created_at'
    )

    def has_add_permission(self, request, obj=None):
        return False

    resource_class = UserSessionResource
admin.site.register(UserSession, UserSessionAdmin)
