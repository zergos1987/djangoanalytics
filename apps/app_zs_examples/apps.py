from json import dumps
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from .models import (
        app_zs_examples_test_table,
        databaseConnections,
        test_table_model,
        processing_module_pipeline_user_content_history,
	)




# Register your models here.
class app_zs_examples_test_tableResource(resources.ModelResource):

    class Meta:
        model = app_zs_examples_test_table
        fields = (
            'test_field',)


class app_zs_examples_test_tableAdmin(ImportExportModelAdmin):
    list_display = [
    	'test_field',]

    list_filter = (
        'test_field',  #('dt', DateTimeRangeFilter)
    )

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )

    resource_class = app_zs_examples_test_tableResource
admin.site.register(app_zs_examples_test_table, app_zs_examples_test_tableAdmin)






# Register your models here.
class test_table_modelResource(resources.ModelResource):

    class Meta:
        model = test_table_model
        fields = (
            'test_field', 'datetime_start_field', 'datetime_end_field', 'boolean_field', 'integer_field', 'integer_choice_field')



class test_table_modelAdmin(ImportExportModelAdmin):
    list_display = [
        'test_field', 'datetime_start_field', 'datetime_end_field', 'boolean_field', 'integer_field', 'integer_choice_field']

    list_filter = (
        'test_field', 'datetime_start_field', 'datetime_end_field', 'boolean_field', 'integer_field', 'integer_choice_field',  #('dt', DateTimeRangeFilter)
    )

    class Media:
        js = ('/static/admin/js/jquery.grp_timepicker.js', )


    resource_class = test_table_modelResource



#dynamic databases-app-mapping code-part
def config(obj):
    return dumps(obj.config)
config.short_description = 'Config'

class databaseConnectionsAdmin(admin.ModelAdmin):
    list_display = ('name', config)





admin.site.register(databaseConnections, databaseConnectionsAdmin)
admin.site.register(test_table_model, test_table_modelAdmin)
admin.site.register(processing_module_pipeline_user_content_history)
