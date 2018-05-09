from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Spreadsheet(models.Model):
	user = models.ForeignKey(User, unique=False, on_delete=models.PROTECT)
	spreadsheet_name = models.CharField(max_length=255)
	spreadsheet_creation_date = models.DateField(default=timezone.now, editable=False)
	spreadsheet_last_modification = models.DateTimeField(default=timezone.now)
	# content = models.TextField()
	# variable_names = models.TextField()
	
class Column(models.Model):
	spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.PROTECT)
	column_name = models.CharField(max_length=255)
	data = models.TextField()

class Plot(models.Model):
	PLOT_TYPES = (
		('B', 'Bar'),
		('L', 'Linear'),
		('S', 'Scatter'),
		('P', 'Pie'),
	)
	
	plot_name = models.CharField(max_length=255)
	plot_creation_date = models.DateField(default=timezone.now, editable=False)
	plot_last_modification = models.DateTimeField(default=timezone.now)
	plot_type = models.CharField(max_length=1, choices=PLOT_TYPES)
	
class PlotData(models.Model):
	PLOTDATA_TYPES = (
		('D', 'DataColumn'),
		('G', 'GroupingColumn'),
	)
	
	plot = models.ForeignKey(Plot, on_delete=models.PROTECT)
	column = models.ForeignKey(Column, on_delete=models.PROTECT)
	type = models.CharField(max_length=1, choices=PLOTDATA_TYPES)

class Report(models.Model):
	user = models.ForeignKey(User, unique=False, on_delete=models.PROTECT)
	report_name = models.CharField(max_length=255)
	report_creation_date = models.DateField(default=timezone.now, editable=False)
	report_last_modification = models.DateTimeField(default=timezone.now)
	
class ReportElementText(models.Model):
	report = models.ForeignKey(Report, on_delete=models.PROTECT)
	element_name = models.CharField(max_length=255)
	text = models.TextField()
	order = models.IntegerField()
	
class ReportElementTable(models.Model):
	TABLE_STYLE = (
		('C', 'Classic'),
		('M', 'Modern'),
		('O', 'Office'),
		('A', 'Alternating'),
	)
	
	report = models.ForeignKey(Report, on_delete=models.PROTECT)
	table_caption = models.CharField(max_length=255)
	style = models.CharField(max_length=1, choices=TABLE_STYLE)
	rows_columns_inverted = models.BooleanField(default=False)
	order = models.IntegerField()
	
class ReportElementTableData(models.Model):
	TABLE_STYLE = (
		('C', 'Classic'),
		('M', 'Modern'),
		('O', 'Office'),
		('A', 'Alternating'),
	)
	
	report = models.ForeignKey(ReportElementTable, on_delete=models.PROTECT)
	column = models.ForeignKey(Column, on_delete=models.PROTECT)
	order = models.IntegerField()	
	
class ReportElementPlot(models.Model):
	report = models.ForeignKey(Report, on_delete=models.PROTECT)
	plot_caption = models.CharField(max_length=255)
	plot = models.ForeignKey(Plot, on_delete=models.PROTECT)
	order = models.IntegerField()
	
class ReportElementReport(models.Model):
	report = models.ForeignKey(Report, related_name='report', on_delete=models.PROTECT)
	embedded_raport_caption = models.CharField(max_length=255)
	embedded_raport = models.ForeignKey(Report, related_name='reportEmbedded', on_delete=models.PROTECT)
	element_start = models.IntegerField()
	element_end = models.IntegerField()
	order = models.IntegerField()