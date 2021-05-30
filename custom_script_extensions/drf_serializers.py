from rest_framework import serializers
from djangoanalytics.apps.examples.models import (
	test_table_model,
	processing_module_pipeline_user_content_history)


class test_table_model__Serializer(serializers.ModelSerializer):
	class Meta:
		model = test_table_model
		fields = ('id', 'test_field', )


class processing_module_pipeline_user_content_history__Serializer(serializers.ModelSerializer):
	class Meta:
		model = processing_module_pipeline_user_content_history
		fields = '__all__'
		#fields = ['id', 'login', 'datetime', 'userobjectparams', 'userobjectwindow']


class Generic__Serializer(serializers.ModelSerializer):
	class Meta:
		model = None
		fields = '__all__'