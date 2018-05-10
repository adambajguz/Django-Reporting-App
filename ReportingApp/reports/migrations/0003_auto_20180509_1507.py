# Generated by Django 2.0.5 on 2018-05-09 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20180509_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spreadsheet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]