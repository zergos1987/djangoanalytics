from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
		app_opensource_surveys_test_table,
	)

# Register your models here.
class app_opensource_surveys_test_tableResource(resources.ModelResource):

    class Meta:
        model = app_opensource_surveys_test_table
        fields = (
            'test_field',)


class app_opensource_surveys_test_tableAdmin(ImportExportModelAdmin):
    list_display = [
    	'test_field',]

    list_filter = (
        'test_field',  #('dt', DateTimeRangeFilter)
    )

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = app_opensource_surveys_test_tableResource
admin.site.register(app_opensource_surveys_test_table, app_opensource_surveys_test_tableAdmin)
