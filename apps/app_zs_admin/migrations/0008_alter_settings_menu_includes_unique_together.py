# Generated by Django 3.2.3 on 2021-06-27 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0007_alter_settings_menu_includes_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='settings_menu_includes',
            unique_together={('name', 'parent_name', 'name_order_by', 'parent_name_order_by')},
        ),
    ]