# Generated by Django 3.2.5 on 2021-08-19 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_interview_scheduled_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='duration_in_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
