# Generated by Django 2.0.4 on 2018-05-31 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20180530_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='plot',
            name='spreadsheet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reports.Spreadsheet'),
            preserve_default=False,
        ),
    ]
