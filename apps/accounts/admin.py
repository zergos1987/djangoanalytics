from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.auth.models import Permission
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _

from .models import (
    app,
	AuditEntry,
    UserSession
	)


# Register your models here.
admin.site.register(Permission)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj #pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']
    date_hierarchy='expire_date'
admin.site.register(Session, SessionAdmin)


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

    model = User

    staff_self_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        # No permissions
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    staff_other_fieldsets = (
        (None, {'fields': ('username', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        # No permissions
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    staff_self_readonly_fields = ('username', 'last_login', 'date_joined')

    def change_view(self, request, object_id, form_url='', extra_context=None, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                if int(object_id) != request.user.id:
                    self.readonly_fields = User._meta.get_all_field_names()
                    self.fieldsets = self.staff_other_fieldsets
                else:
                    self.readonly_fields = self.staff_self_readonly_fields
                    self.fieldsets = self.staff_self_fieldsets

                response = super(CustomUserAdmin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)
            except:
                pass
                #logger.error('Admin change view error. Returned all readonly fields')

                self.fieldsets = self.staff_other_fieldsets
                self.readonly_fields = ('first_name', 'last_name', 'email', 'username', 'password', 'last_login', 'date_joined')
                response = super(CustomUserAdmin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserAdmin.fieldsets
                self.readonly_fields = UserAdmin.readonly_fields
            return response
        else:
            return super(CustomUserAdmin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)
    # readonly_fields = [
    #     'date_joined',
    #     'last_login',
    # ]

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     is_superuser = request.user.is_superuser
    #     disabled_fields = set()  # type: Set[str]

    #     if not is_superuser:
    #         disabled_fields |= {
    #             'username',
    #             'is_staff',
    #             'is_superuser',
    #         }

    #     for f in disabled_fields:
    #         if f in form.base_fields:
    #             form.base_fields[f].disabled = True

    #     return form

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
