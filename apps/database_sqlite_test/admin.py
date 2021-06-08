from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
		database_sqlite_test_test_table,
	)

# Register your models here.
class database_sqlite_test_test_tableResource(resources.ModelResource):

    class Meta:
        model = database_sqlite_test_test_table
        fields = (
            'test_field',)


class database_sqlite_test_test_tableAdmin(ImportExportModelAdmin):
    list_display = [
    	'test_field',]

    list_filter = (
        'test_field',  #('dt', DateTimeRangeFilter)
    )

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = database_sqlite_test_test_tableResource
admin.site.register(database_sqlite_test_test_table, database_sqlite_test_test_tableAdmin)
