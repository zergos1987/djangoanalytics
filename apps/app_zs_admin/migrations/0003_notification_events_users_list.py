# Generated by Django 3.2.6 on 2021-08-26 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_zs_admin', '0002_notification_events_user_notification_event_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification_events',
            name='users_list',
            field=models.ManyToManyField(blank=True, related_name='for_user_notification_event_show', to='app_zs_admin.aside_left_menu_includes'),
        ),
    ]