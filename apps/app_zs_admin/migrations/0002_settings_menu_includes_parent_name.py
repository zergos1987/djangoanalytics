# Generated by Django 3.2.3 on 2021-06-27 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings_menu_includes',
            name='parent_name',
            field=models.CharField(default=' ', max_length=200),
            preserve_default=False,
        ),
    ]
