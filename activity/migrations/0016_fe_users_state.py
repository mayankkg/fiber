# Generated by Django 4.0.3 on 2022-06-10 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0015_activity_client_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='fe_users',
            name='state',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]