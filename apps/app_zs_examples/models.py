from django.db import models


# Create your models here.


class app_zs_examples_test_table(models.Model):
    test_field = models.CharField(max_length=150)

    class Meta:
    	# app_label helps django to recognize your db
    	app_label = 'app_zs_examples'


    def __str__(self):
        return self.test_field
