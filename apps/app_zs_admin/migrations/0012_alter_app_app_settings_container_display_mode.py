# Generated by Django 3.2.6 on 2021-11-23 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0011_auto_20211001_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='app_settings_container_display_mode',
            field=models.ManyToManyField(blank=True, to='app_zs_admin.container_display_mode'),
        ),
    ]