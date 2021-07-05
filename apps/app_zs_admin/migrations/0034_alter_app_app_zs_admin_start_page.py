# Generated by Django 3.2.3 on 2021-07-02 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0033_rename_app_start_page_app_app_zs_admin_start_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='app_zs_admin_start_page',
            field=models.CharField(blank=True, choices=[('app_zs_admin', 'app_zs_admin'), ('app_opensource_dashboards', 'app_opensource_dashboards'), ('app_opensource_surveys', 'app_opensource_surveys'), ('app_zs_dashboards', 'app_zs_dashboards'), ('app_zs_examples', 'app_zs_examples'), ('database_oracle_sadko', 'database_oracle_sadko'), ('database_sqlite_test', 'database_sqlite_test')], max_length=70, null=True),
        ),
    ]
