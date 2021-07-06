# Generated by Django 3.2.3 on 2021-06-29 20:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_zs_admin', '0019_alter_aside_left_menu_includes_url_groups_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aside_left_menu_includes',
            name='url_groups_permissions',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]