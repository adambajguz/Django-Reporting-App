# Generated by Django 2.0.5 on 2018-05-10 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20180510_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotdata',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Column'),
        ),
        migrations.AlterField(
            model_name='plotdata',
            name='plot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Plot'),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reportelementplot',
            name='plot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Plot'),
        ),
        migrations.AlterField(
            model_name='reportelementplot',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Report'),
        ),
        migrations.AlterField(
            model_name='reportelementreport',
            name='embedded_raport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportEmbedded', to='reports.Report'),
        ),
        migrations.AlterField(
            model_name='reportelementreport',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='reports.Report'),
        ),
        migrations.AlterField(
            model_name='reportelementtable',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Report'),
        ),
        migrations.AlterField(
            model_name='reportelementtabledata',
            name='column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Column'),
        ),
        migrations.AlterField(
            model_name='reportelementtabledata',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.ReportElementTable'),
        ),
        migrations.AlterField(
            model_name='reportelementtext',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Report'),
        ),
        migrations.AlterField(
            model_name='spreadsheet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
