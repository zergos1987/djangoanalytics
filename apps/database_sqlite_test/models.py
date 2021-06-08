from django.db import models


# Create your models here.


class database_sqlite_test_test_table(models.Model):
    test_field = models.CharField(max_length=150)

    class Meta:
    	# app_label helps django to recognize your db
    	app_label = 'database_sqlite_test'


    def __str__(self):
        return self.test_field
