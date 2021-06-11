from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
		app,
	)

# Register your models here.
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
        
