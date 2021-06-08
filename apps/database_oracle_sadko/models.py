from django.db import models


# Create your models here.


class database_oracle_sadko_test_table(models.Model):
    test_field = models.CharField(max_length=150)

    class Meta:
    	# app_label helps django to recognize your db
    	app_label = 'database_oracle_sadko'


    def __str__(self):
        return self.test_field
