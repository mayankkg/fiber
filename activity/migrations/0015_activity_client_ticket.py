# Generated by Django 4.0.3 on 2022-06-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0014_activity_revised_ecd'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='client_ticket',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]