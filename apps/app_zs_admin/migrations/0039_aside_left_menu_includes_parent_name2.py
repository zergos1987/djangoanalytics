# Generated by Django 3.2.3 on 2021-07-11 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0038_auto_20210708_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='aside_left_menu_includes',
            name='parent_name2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_zs_admin.aside_left_menu_includes'),
        ),
    ]
