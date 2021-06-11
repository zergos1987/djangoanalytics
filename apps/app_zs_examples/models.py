from django.db import models
from jsonfield import JSONField


# Create your models here.
class app(models.Model):
    test_field = models.CharField(max_length=150)

    class Meta:
    	# app_label helps django to recognize your db
    	app_label = 'app_zs_examples'


    def __str__(self):
        return self.test_field



class databaseConnections(models.Model):
    name = models.CharField(max_length=256, unique=True)
    config = JSONField()

    class Meta:
        # app_label helps django to recognize your db
        app_label = 'app_zs_examples'


    def __unicode__(self):
        return self.name



class test_table_model(models.Model):

    class choice_list(models.IntegerChoices):
        value_one = 1
        value_two = 2
        value_three = 3
        value_four = 4

    test_field = models.CharField(max_length=150)
    datetime_start_field = models.DateTimeField(null=True, blank=True)
    datetime_end_field = models.DateTimeField(null=True, blank=True)
    boolean_field = models.BooleanField(default=True)
    integer_field = models.IntegerField(null=True, blank=True)
    integer_choice_field = models.IntegerField(choices=choice_list.choices, default=0)


    class Meta:
    	# app_label helps django to recognize your db
    	app_label = 'app_zs_examples'

    # def __str__(self):
    #     return self.test_field

    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (
            self.test_field, 
            self.datetime_start_field,
            self.datetime_end_field, 
            self.boolean_field, 
            self.integer_field, 
            self.integer_choice_field)



class processing_module_pipeline_user_content_history(models.Model):
    login = models.CharField(max_length=250, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    userobject = models.CharField(max_length=750, null=True, blank=True)
    userobjectparams = models.CharField(max_length=1500, null=True, blank=True)
    userobjectwindow = models.CharField(max_length=30, null=True, blank=True)


    class Meta:
        app_label = 'app_zs_examples'
        db_table = 'processing_module_pipeline_user_content_history'
        
        
    def __str__(self):
        return str(self.login) if self.login else ''
