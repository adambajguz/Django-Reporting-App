# Generated by Django 2.0.4 on 2018-05-30 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='plot_last_modification',
            field=models.DateTimeField(auto_now=True),
        ),
    ]