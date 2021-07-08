# Generated by Django 3.2.3 on 2021-07-05 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_app'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_extra_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=300, null=True)),
                ('department', models.CharField(blank=True, max_length=800, null=True)),
                ('center', models.CharField(blank=True, max_length=800, null=True)),
                ('position', models.CharField(blank=True, max_length=800, null=True)),
                ('name', models.CharField(blank=True, max_length=300, null=True)),
                ('last_name', models.CharField(blank=True, max_length=300, null=True)),
                ('ldap_groups', models.CharField(blank=True, max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]