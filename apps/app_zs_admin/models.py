from django.db import models
from colorfield.fields import ColorField
from jsonfield import JSONField

# Create your models here.

class app(models.Model):
	app_brand_name = models.CharField(max_length=400, default='DjangoAnalytics')
	app_brand_color = ColorField(default='#333')
	app_brand_ico = models.ImageField(upload_to='img', null=True)
	app_brand_logo = models.ImageField(upload_to='img', null=True)
	app_breadcrumb_active = models.CharField(max_length=400, default='', blank=True)
	app_settings = JSONField(default=list, null=True, blank=True)
	is_actual = models.BooleanField(default=False)

	class Meta:
		# app_label helps django to recognize your db
		app_label = 'app_zs_admin'
		unique_together = ('app_brand_name', 'app_brand_ico', 'app_brand_logo', 'app_breadcrumb_active')

	def save(self, *args, **kwargs):
		if self.is_actual:
			try:
				x = app.objects.filter(is_actual=True).exclude(id=self.id).update(is_actual=False)
			except Exception as e:
				pass
		super(app, self).save(*args, **kwargs)

	def __str__(self):
		field_values = []
		for field in self._meta.get_fields():
			field_values.append(str(getattr(self, field.name, '')))
		field_values = ['app_brand_name', 'is_actual',]
		return ' '.join(field_values)
