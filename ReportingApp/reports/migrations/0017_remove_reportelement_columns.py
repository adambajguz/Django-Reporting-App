# Generated by Django 2.0.5 on 2018-06-04 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0016_report_report_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportelement',
            name='columns',
        ),
    ]