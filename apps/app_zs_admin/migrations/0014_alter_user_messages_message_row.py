# Generated by Django 3.2.6 on 2021-11-26 22:40

import apps.app_zs_admin.models
from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0013_user_message_headers_user_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_messages',
            name='message_row',
            field=jsonfield.fields.JSONField(blank=True, default=apps.app_zs_admin.models.default_message_row, null=True),
        ),
    ]
