# Generated by Django 3.2.3 on 2021-07-01 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0028_auto_20210701_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aside_left_menu_includes',
            name='render_app_name',
            field=models.CharField(blank=True, choices=[('zs_admin', 'zs_admin'), ('os_dashboards', 'os_dashboards'), ('op_surveys', 'op_surveys'), ('zs_dashboards', 'zs_dashboards'), ('zs_examples', 'zs_examples'), ('database_oracle_sadko', 'database_oracle_sadko'), ('database_sqlite_test', 'database_sqlite_test')], max_length=70, null=True),
        ),
    ]