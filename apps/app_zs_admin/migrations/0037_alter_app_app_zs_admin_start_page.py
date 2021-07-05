# Generated by Django 3.2.3 on 2021-07-02 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0036_alter_app_app_zs_admin_start_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='app_zs_admin_start_page',
            field=models.CharField(choices=[('zs_admin', 'zs_admin'), ('accounts', 'accounts'), ('os_dashboards', 'os_dashboards'), ('os_surveys', 'os_surveys'), ('zs_dashboards', 'zs_dashboards'), ('zs_examples', 'zs_examples'), ('db_sadko', 'db_sadko'), ('db_sqlite_test', 'db_sqlite_test')], default='zs_admin', max_length=70, null=True),
        ),
    ]
