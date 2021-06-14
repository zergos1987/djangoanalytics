from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _

from .models import (
    app,
	AuditEntry,
    UserSession
	)


# Register your models here.
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

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)






print('Session', [field.name for field in Session._meta.get_fields()])
print('Group', [field.name for field in Group._meta.get_fields()])
print('Permission', [field.name for field in Permission._meta.get_fields()])
print('UserSession', [field.name for field in UserSession._meta.get_fields()])



class app_Resource(resources.ModelResource):
    class Meta:
        model = app
        fields = ('id',)


class app_Admin(ImportExportModelAdmin):
    list_display = ['id']
    list_filter = ('id', )

    def has_add_permission(self, request, obj=None):
        return False

    resource_class = app_Resource

admin.site.register(app, app_Admin)


class Permission_Resource(resources.ModelResource):
    class Meta:
        model = Permission
        fields = ('id', 'content_type', 'name', 'codename',)


class Permission_Admin(ImportExportModelAdmin):


class Permission_Admin(ImportExportModelAdmin):
    def content_type_app_model_id(self, obj):
        return obj.content_type.app_label + ' | ' + obj.content_type.model + ' | ' + str(obj.content_type.id)
    content_type_app_model_id.short_description  = 'APP | Model | id'

    list_display = ('id', 'content_type_app_model_id', 'name', 'codename', )
    list_filter = ('id', 'content_type', 'name', 'codename', )
    search_fields = ['name', 'codename', 'content_type__app_label', 'content_type__model']

    def has_add_permission(self, request, obj=None):
        return False

    resource_class = Permission_Resource

admin.site.register(Permission, Permission_Admin)




class Group_Resource(resources.ModelResource):
    class Meta:
        model = Group
        fields = ('id', 'name',)


class Group_Admin(ImportExportModelAdmin):
    
    list_display = ['id', 'name']
    list_filter = ('id', 'name',)
    search_fields = ['name',]

    def has_add_permission(self, request, obj=None):
        return False

    resource_class = Group_Resource

admin.site.unregister(Group)
admin.site.register(Group, Group_Admin)




class Session_Resource(resources.ModelResource):
    class Meta:
        model = Session
        fields = ('session_key', 'expire_date', )


class Session_Admin(ImportExportModelAdmin):
    
    list_display = ['session_key', 'expire_date']
    list_filter = ('session_key', 'expire_date', )
    exclude = ['session_data']
    date_hierarchy='expire_date'

    def has_add_permission(self, request, obj=None):
        return False

    resource_class = Session_Resource

admin.site.register(Session, Session_Admin)




class UserSession_Resource(resources.ModelResource):
    class Meta:
        model = UserSession
        fields = ('user', 'session',)


class UserSession_Admin(ImportExportModelAdmin):
    list_display = ['user', 'session', 'created_at', 'remove_session']
    list_filter = ('user', 'session', 'created_at',)
    #search_fields = ['user', 'session', 'created_at',]

    def has_add_permission(self, request, obj=None):
        return False

    resource_class = UserSession_Resource

admin.site.register(UserSession, UserSession_Admin)




class AuditEntry_Resource(resources.ModelResource):
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


class AuditEntry_Admin(ImportExportModelAdmin):
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
    list_filter = ('dt', 'action', 'request_method', 'request_method',)
    search_fields = ['action', 'request_method', 'username', 'ip', 'device', 'browser_family', 'browser_version', 'os_family', 'os_version',]

    def has_add_permission(self, request, obj=None):
        return False

    resource_class = AuditEntry_Resource

admin.site.register(AuditEntry, AuditEntry_Admin)
