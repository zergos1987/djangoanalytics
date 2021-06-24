from django.db import models
from colorfield.fields import ColorField
from jsonfield import JSONField

# Create your models here.

class app(models.Model):
	app_brand_name = models.CharField(max_length=400, null=True)
	app_brand_color = ColorField(default='#333')
	app_brand_ico = models.ImageField(upload_to='img', null=True)
	app_brand_logo = models.ImageField(upload_to='img', null=True)
	app_settings = JSONField(default=dict)
	is_actual = models.BooleanField(default=False)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'


	def __str__(self):
		field_values = []
		for field in self._meta.get_fields():
			field_values.append(str(getattr(self, field.name, '')))
		field_values = ['app_brand_name', 'is_actual',]
		return ' '.join(field_values)
