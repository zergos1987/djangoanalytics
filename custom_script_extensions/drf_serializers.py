from rest_framework import serializers

from apps.app_zs_examples.models import (
	test_table_model, 
	processing_module_pipeline_user_content_history,)

from apps.app_zs_admin.models import (
    etl_job_database_tables_tasks,
    week_intervals,
    time_intervals)



class week_intervals__Serializer(serializers.ModelSerializer):
     class Meta:
        model = week_intervals
        fields = ['id', 'update_week_days_list',]



class time_intervals__Serializer(serializers.ModelSerializer):
     class Meta:
        model = time_intervals
        fields = ['id', 'update_time_list',]



class etl_job_database_tables_tasks__Serializer(serializers.ModelSerializer):
    update_week_days_list = week_intervals__Serializer(many=True, read_only=False)
    update_time_list = time_intervals__Serializer(many=True, read_only=False)

    class Meta:
        model = etl_job_database_tables_tasks
        #fields = '__all__'
        fields = ['id', 'limit_rows', 'update_week_days_list', 'update_time_list',
            'database_name_from', 'database_name_to','table_schema_from','table_schema_to','table_name_prefix',
            'table_name_from','create_table_if_not_exists','where_condition_from',
            'where_condition_to','columns_from','columns_for_unique_id','clear_all_data_before_insert',
            'remove_duplicates_table_to','update_exists_rows','insert_only_new_rows','insert_all_rows',
            'drop_table_to','steps_delay_seconds','created_by','created_date','updated_by','updated_date','etl_error_flag','is_actual'
        ]
        #fields = ['id', "login", "datetime", "userobjectparams", "userobjectwindow"]
        #depth = 1

class etl_job_database_tables_tasks__update_create_Serializer(serializers.ModelSerializer):

    class Meta:
        model = etl_job_database_tables_tasks
        fields = etl_job_database_tables_tasks__Serializer.Meta.fields





class processing_module_pipeline_user_content_history__Serializer(serializers.ModelSerializer):
    class Meta:
        model = processing_module_pipeline_user_content_history
        fields = '__all__'
        #fields = ['id', "login", "datetime", "userobjectparams", "userobjectwindow"]




class test_table_model__Serializer(serializers.ModelSerializer):
    class Meta:
        model = test_table_model
        fields = ('id', 'test_field', 'datetime_start_field', 'datetime_end_field', 'boolean_field', 'integer_field', 'integer_choice_field',)




class Generic__Serializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
