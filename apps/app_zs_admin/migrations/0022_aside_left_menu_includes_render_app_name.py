# Generated by Django 3.2.3 on 2021-06-29 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0021_auto_20210629_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='aside_left_menu_includes',
            name='render_app_name',
            field=models.CharField(choices=[('os_dashboards', 'os_dashboards'), ('zs_dashboards', 'zs_dashboards'), ('zs_examples', 'zs_examples')], default='app_zs_admin', max_length=15),
        ),
    ]
