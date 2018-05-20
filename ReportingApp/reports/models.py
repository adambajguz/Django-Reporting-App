from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Spreadsheet(models.Model):
	user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
	spreadsheet_name = models.CharField(max_length=255)
	spreadsheet_description = models.TextField(default='')
	spreadsheet_creation_date = models.DateField(auto_now_add=True, editable=False)
	spreadsheet_last_modification = models.DateTimeField(auto_now=True)


	@classmethod
	def create(cls, user):
		spreadsheets_count = len(Spreadsheet.objects.filter(user__id = user.id))

		new_spreadsheet = Spreadsheet.objects.create(spreadsheet_name='New Spreadsheet #' + str(spreadsheets_count + 1), user=user)

		Column.add_multiple_columns(new_spreadsheet, num_cells=10, num_columns=5)

		return new_spreadsheet

	def last_modification_days_ago(self):
		time = timezone.now()
		format_str=""
		if self.spreadsheet_last_modification.day == time.day:
			hours = time.hour - self.spreadsheet_last_modification.hour

			if hours == 0:
				return "less than an hour ago"
			elif hours == 1:
				format_str = " hour ago"
			else:
				format_str = " hours ago"

			return str(hours) + format_str
		else:
			if self.spreadsheet_last_modification.month == time.month:
				days = time.day - self.spreadsheet_last_modification.day

				if days == 0:
					return "yesterday"
				elif days == 1:
					format_str = " day ago"
				else:
					format_str = " days ago"
				return str(days) + format_str
			else:
				if self.spreadsheet_last_modification.year == time.year:
					months = time.month - self.spreadsheet_last_modification.month

					if months == 0:
						return "this month"
					elif months == 1:
						format_str = " month ago"
					else:
						format_str = " months ago"
					return str(months) + format_str
				else:
					years = time.year - self.spreadsheet_last_modification.year

					if years == 0:
						return "this year"
					elif years == 1:
						format_str = " year ago"
					else:
						format_str = " years ago"
					return str(years) + format_str
		return self.spreadsheet_last_modification

class Column(models.Model):
	spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)
	column_name = models.CharField(max_length=255)

	@classmethod
	def add_multiple_columns(cls, spreadsheet, num_cells, num_columns):
		for _ in range(0, num_columns):
			cls.add_column(spreadsheet, num_cells)

	@classmethod	
	def add_column(cls, spreadsheet, num_cells):
		columns = Column.objects.filter(spreadsheet__id = spreadsheet.id)

		col = Column.objects.create(spreadsheet=spreadsheet, column_name="New column #" + str(columns.count()))
		for _ in range(0, num_cells):
			Cell.objects.create(column=col)

class Cell(models.Model):
	contents = models.CharField(max_length=256, default='', blank=True, null=True)
	column = models.ForeignKey(Column, related_name='cells', on_delete=models.CASCADE)

class Plot(models.Model):
	PLOT_TYPES = (
		('B', 'Bar'),
		('L', 'Linear'),
		('S', 'Scatter'),
		('P', 'Pie'),
	)

	plot_name = models.CharField(max_length=255)
	plot_creation_date = models.DateField(auto_now_add=True, editable=False)
	plot_last_modification = models.DateTimeField(auto_now_add=True)
	plot_type = models.CharField(max_length=1, choices=PLOT_TYPES)

class PlotData(models.Model):
	PLOTDATA_TYPES = (
		('D', 'DataColumn'),
		('G', 'GroupingColumn'),
	)

	plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
	column = models.ForeignKey(Column, on_delete=models.CASCADE)
	type = models.CharField(max_length=1, choices=PLOTDATA_TYPES)

class Report(models.Model):
	user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
	report_name = models.CharField(max_length=255)
	report_creation_date = models.DateField(auto_now_add=True, editable=False)
	report_last_modification = models.DateTimeField(auto_now_add=True)

class ReportElementText(models.Model):
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
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

	report = models.ForeignKey(Report, on_delete=models.CASCADE)
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

	report = models.ForeignKey(ReportElementTable, on_delete=models.CASCADE)
	column = models.ForeignKey(Column, on_delete=models.CASCADE)
	order = models.IntegerField()

class ReportElementPlot(models.Model):
	report = models.ForeignKey(Report, on_delete=models.CASCADE)
	plot_caption = models.CharField(max_length=255)
	plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
	order = models.IntegerField()

class ReportElementReport(models.Model):
	report = models.ForeignKey(Report, related_name='report', on_delete=models.CASCADE)
	embedded_raport_caption = models.CharField(max_length=255)
	embedded_raport = models.ForeignKey(Report, related_name='reportEmbedded', on_delete=models.CASCADE)
	element_start = models.IntegerField()
	element_end = models.IntegerField()
	order = models.IntegerField()
