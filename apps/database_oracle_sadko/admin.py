from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
		database_oracle_sadko_test_table,
	)

# Register your models here.
class database_oracle_sadko_test_tableResource(resources.ModelResource):

    class Meta:
        model = database_oracle_sadko_test_table
        fields = (
            'test_field',)


class database_oracle_sadko_test_tableAdmin(ImportExportModelAdmin):
    list_display = [
    	'test_field',]

    list_filter = (
        'test_field',  #('dt', DateTimeRangeFilter)
    )

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = database_oracle_sadko_test_tableResource
admin.site.register(database_oracle_sadko_test_table, database_oracle_sadko_test_tableAdmin)
