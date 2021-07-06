from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.db.models import Q
import logging

from .models import (
    app,
	AuditEntry,
    UserSession,
    user_extra_details
	)

logger = logging.getLogger(__name__)

# Register your models here.
class app_Resource(resources.ModelResource):
    class Meta:
        model = app
        fields = ('id',)


class app_Admin(ImportExportModelAdmin):
    
    list_per_page = 15
    list_display = ['id']
    list_filter = ('id', )
    
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

    resource_class = app_Resource

admin.site.register(app, app_Admin)




class Group_Resource(resources.ModelResource):
    class Meta:
        model = Group
        fields = ('id', 'name',)


class Group_Admin(ImportExportModelAdmin):
    
    list_per_page = 15
    list_display = ['id', 'name']
    list_filter = ('id', 'name',)
    search_fields = ['name',]
    ordering = ('name',)

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

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    resource_class = Group_Resource

admin.site.unregister(Group)
admin.site.register(Group, Group_Admin)




class Permission_Resource(resources.ModelResource):
    class Meta:
        model = Permission
        fields = ('id', 'content_type', 'name', 'codename',)


class Permission_Admin(ImportExportModelAdmin):
    
    list_per_page = 15

    def content_type_app_model_id(self, obj):
        return obj.content_type.app_label + ' | ' + obj.content_type.model + ' | ' + str(obj.content_type.id)
    content_type_app_model_id.short_description  = 'APP | Model | id'
    content_type_app_model_id.admin_order_field = 'id'

    list_display = ('id', 'content_type_app_model_id', 'name', 'codename', )
    list_filter = ('id', 'content_type', 'name', 'codename', )
    search_fields = ['name', 'codename', 'content_type__app_label', 'content_type__model']

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

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    resource_class = Permission_Resource

admin.site.register(Permission, Permission_Admin)




class CustomUser_Resource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_statff', 'last_login', 'is_active', )


class CustomUser_Admin(ImportExportModelAdmin, UserAdmin):

    model = User

    list_per_page = 15
    list_display = ['id', 'username', 'email',  'last_login', 'is_active']
    list_filter = (
        ('date_joined', DateRangeFilter), 
        'is_active', 'is_staff', 'is_superuser', 'groups',
    )
    ordering = ('-date_joined', 'username',)
    date_hierarchy = 'date_joined'
    search_fields = ['username', 'first_name', 'last_name', 'email', 'last_login',]
    actions = ['ban_users', 'remove_ban', 'export_as_json']

    staff_userEditor_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', )}),
        (_('Permissions'), {'fields': ('is_active', 'groups', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

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

    def render_change_form(self, request, context, *args, **kwargs):
        if not request.user.is_superuser:
            if len(context['adminform'].form.fields) > 0:
                if context['adminform'].form.fields.get('groups', None):
                    remove_list_from_results = ['admin_viewer_group', 'admin_editor_group', 'admin_creator_group', 'admin_api_group']
                    queryset_ids = Group.objects.values_list('id', flat=True).exclude(~Q(name__in=remove_list_from_results))
                    queryset_ids = [int(ids) for ids in queryset_ids]
                    context['adminform'].form.fields['groups'].queryset = Group.objects.exclude(id__in=queryset_ids)
        return super(CustomUser_Admin, self).render_change_form(request, context, args, kwargs)

    def change_view(self, request, object_id, form_url='', extra_context=None, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                opts = self.opts
                codename = get_permission_codename('change', opts)
                edited_user = User.objects.filter(id=object_id).first()
                # User who have change perm can change non-staff Users and not self
                if request.user.has_perm("%s.%s" % (opts.app_label, codename)) and edited_user.id != request.user.id and not (edited_user.is_staff or edited_user.is_superuser):
                    self.readonly_fields = self.staff_self_readonly_fields
                    self.fieldsets = self.staff_userEditor_fieldsets

                elif int(object_id) != request.user.id:
                    self.readonly_fields = User._meta.NOT_get_fields() #get_fields()
                    self.fieldsets = self.staff_other_fieldsets
                else:
                    self.readonly_fields = self.staff_self_readonly_fields
                    self.fieldsets = self.staff_self_fieldsets

                response = super(CustomUser_Admin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)
            except:
                pass
                logger.error('Admin change view error. Returned all readonly fields')

                self.fieldsets = self.staff_other_fieldsets
                self.readonly_fields = ('first_name', 'last_name', 'email', 'username', 'password', 'last_login', 'date_joined')
                response = super(CustomUser_Admin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserAdmin.fieldsets
                self.readonly_fields = UserAdmin.readonly_fields
            return response
        else:
            return super(CustomUser_Admin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)

    #@admin.action(permissions=['can_ban_users'])
    def ban_users(self, request, queryset):
        #banned_user = Banned_User.objects.create(profile=request.user.profile)
        #banned_user.save()
        #self.message_user(request, f"{u_count}  Users was banned")
        u_count = queryset.filter(is_active=True, is_superuser=False).update(is_active = False)
        supersuser_count = queryset.filter(is_active=True, is_superuser=True)

        self.message_user(request, ngettext(
            '%d User was banned.',
            '%d Users was banned.',
            u_count,
        ) % u_count, messages.SUCCESS)
        if len(supersuser_count) > 0:
            self.message_user(request, ngettext(
                '%d Superuser cannot be banned.',
                '%d Superusers cannot be banned.',
                len(supersuser_count),
            ) % len(supersuser_count), messages.WARNING)
    ban_users.allowed_permissions = ['can_ban_users']
    ban_users.short_description = 'Заблокировать пользователя'


    #@admin.action(permissions=['can_unban_users'])
    def remove_ban(self, request, queryset):
        u_count = queryset.filter(is_active=False).update(is_active = True)
        #self.message_user(request, f"{u_count} - Users was unbanned")
        self.message_user(request, ngettext(
            '%d User was unbanned.',
            '%d Users was unbanned.',
            u_count,
        ) % u_count, messages.SUCCESS)
    remove_ban.allowed_permissions = ['can_unban_users']
    remove_ban.short_description = 'Разблокировать пользователя'


    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response
    export_as_json.short_description = 'Экспорт в JSON URL'

    def has_can_ban_users_permission(self, request):
        """Does the user have the publish permission?"""
        opts = self.opts
        codename = get_permission_codename('can_ban_users', opts)
        #return request.user.has_perm('%s.%s' % (opts.app_label, codename))
        return request.user.has_perm("accounts.can_ban_users")

    def has_can_unban_users_permission(self, request):
        """Does the user have the publish permission?"""
        opts = self.opts
        codename = get_permission_codename('can_unban_users', opts)
        #return request.user.has_perm('%s.%s' % (opts.app_label, codename))
        return request.user.has_perm("accounts.can_unban_users")

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

    # def has_add_permission(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     else:
    #         return False

    def has_change_permission(self, request, obj=None):
        return True
        # opts = self.opts
        # codename1 = get_permission_codename('add', opts)
        # codename2 = get_permission_codename('change', opts)
        # if request.user.is_superuser:
        #     return True
        # else:
        #     return request.user.has_perm("%s.%s" % (opts.app_label, codename1)) or request.user.has_perm("%s.%s" % (opts.app_label, codename2))

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    class Media:
        js = ('accounts/origin/js/index.js', )  
        css = {'all': ('accounts/origin/css/index.css',)}

    resource_class = CustomUser_Resource

admin.site.unregister(User)
admin.site.register(User, CustomUser_Admin)





class user_extra_details_Resource(resources.ModelResource):
    class Meta:
        model = user_extra_details
        fields = ('user', 'full_name', 'department', 
            'center', 'position', 'name', 'last_name', 'ldap_is_active',)

class user_extra_details_Admin(ImportExportModelAdmin):
    list_per_page = 15
    list_display = ['user', 'full_name', 'department', 'center', 'position', 'name', 'last_name', 'ldap_is_active']
    list_filter = ('department', 'center', 'position', 'ldap_is_active',)
    search_fields = ['user',  'full_name', 'department', 'center', 'position']
    
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

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
            
    resource_class = user_extra_details_Resource

admin.site.register(user_extra_details, user_extra_details_Admin)




class Session_Resource(resources.ModelResource):
    class Meta:
        model = Session
        fields = ('session_key', 'expire_date', )

class Session_Admin(ImportExportModelAdmin):
    
    list_per_page = 15
    model = Session

    list_display = ['session_key', 'expire_date']
    list_filter = ('session_key', ('expire_date', DateRangeFilter), )
    ordering = ('expire_date',)
    date_hierarchy = 'expire_date'

    search_fields = ['session_key', 'expire_date',]

    staff_self_fieldsets = (
        (None, {'fields': ('session_key', 'expire_date',)}),
    )

    staff_other_fieldsets = (
        (None, {'fields': ('session_key', 'expire_date',)}),
    )

    staff_self_readonly_fields = ('session_key', 'expire_date', )

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

                response = super(Session_Admin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)
            except:
                pass
                #logger.error('Admin change view error. Returned all readonly fields')

                self.fieldsets = self.staff_other_fieldsets
                self.readonly_fields = ('session_key', 'expire_date', )
                response = super(Session_Admin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = Session_Admin.fieldsets
                self.readonly_fields = Session_Admin.readonly_fields
            return response
        else:
            return super(Session_Admin, self).change_view(request, object_id, form_url, extra_context, *args, **kwargs)


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

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    resource_class = Session_Resource

admin.site.register(Session, Session_Admin)





class UserSession_Resource(resources.ModelResource):
    class Meta:
        model = UserSession
        fields = ('user', 'session',)

class UserSession_Admin(ImportExportModelAdmin):
    list_per_page = 15
    list_display = ['user', 'session', 'created_at', 'remove_session']
    list_filter = ('user', 'session', ('created_at', DateRangeFilter),)
    #search_fields = ['user', 'session', 'created_at',]
    
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

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
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
    list_per_page = 15
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

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    resource_class = AuditEntry_Resource

admin.site.register(AuditEntry, AuditEntry_Admin)
