# Generated by Django 3.2.6 on 2021-09-14 19:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0005_notification_events_event_content2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aside_left_menu_includes',
            options={'ordering': ('parent_name_order_by', 'name_order_by', '-menu_icon_type')},
        ),
        migrations.AlterField(
            model_name='notification_events',
            name='event_content2',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
    ]