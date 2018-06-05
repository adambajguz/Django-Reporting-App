from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

from reports.charts import *

class Spreadsheet(models.Model):
	user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
	spreadsheet_name = models.CharField(max_length=255)
	spreadsheet_description = models.TextField(default='')
	spreadsheet_creation_date = models.DateField(auto_now_add=True, editable=False)
	spreadsheet_last_modification = models.DateTimeField(auto_now=True)

	row_number = models.IntegerField(default=5)
	column_number = models.IntegerField(default=0)

	class Meta:
		indexes = [
			models.Index(fields=['user']),
		]	

	def __str__(self):
		return self.spreadsheet_name

	@classmethod
	def create(cls, user):
		spreadsheets_count = Spreadsheet.objects.filter(user__id = user.id).count()

		new_spreadsheet = Spreadsheet.objects.create(spreadsheet_name='New Spreadsheet #' + str(spreadsheets_count + 1), user=user)

		Column.add_multiple_columns_and_cells(new_spreadsheet, num_cells=5, num_columns=3)

		return new_spreadsheet

	def table(self):
		columns = Column.objects.filter(spreadsheet__id = self.id)

		rows = []
		for current_column in columns:
			cells = current_column.cells.all()
			rows.append(cells.values_list('contents', flat=True))

		return {'num_rows': range(0, self.row_number),
				'rows': rows,
				'columns': columns,}


class Column(models.Model):
	spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE)
	column_name = models.CharField(max_length=255)

	class Meta:
		indexes = [
			models.Index(fields=['spreadsheet']),
		]	

	@classmethod
	def add_multiple_columns(cls, spreadsheet, num_columns):
		for _ in range(0, num_columns):
			cls.add_column(spreadsheet)

	@classmethod
	def add_multiple_columns_and_cells(cls, spreadsheet, num_cells, num_columns):
		for _ in range(0, num_columns):
			cls.add_column_and_cells(spreadsheet, num_cells)

	@classmethod	
	def add_column(cls, spreadsheet):
		row_num = spreadsheet.row_number

		return cls.add_column_and_cells(spreadsheet, row_num)

	@classmethod	
	def add_column_and_cells(cls, spreadsheet, num_cells):
		col_num = spreadsheet.column_number

		new_col = Column.objects.create(spreadsheet=spreadsheet, column_name="New column #" + str(col_num))
		# for _ in range(0, num_cells):
		# 	Cell.objects.create(column=new_col)

		cell_data = {"column": new_col}
		cell_list = [Cell(**cell_data) for i in range(0, num_cells)]
		Cell.objects.bulk_create(cell_list)

		spreadsheet.column_number = col_num + 1
		spreadsheet.save()

		return new_col

class Cell(models.Model):
	contents = models.CharField(max_length=256, default='', blank=True, null=True)
	column = models.ForeignKey(Column, related_name='cells', on_delete=models.CASCADE)

	class Meta:
		indexes = [
			models.Index(fields=['contents']),
		]

class Plot(models.Model):
	PLOT_TYPES = (
		('B', 'Bar'),
		('L', 'Linear'),
		('P', 'Pie'),
		('R', 'Radar'),
		('X', 'Box'),
		('Y', 'Pyramid'),
	)

	user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
	
	spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, null=True, blank=True)

	plot_name = models.CharField(max_length=255)
	plot_creation_date = models.DateField(auto_now_add=True, editable=False)
	plot_last_modification = models.DateTimeField(auto_now=True)
	plot_type = models.CharField(max_length=1, choices=PLOT_TYPES, default='B')

	data_columns = models.TextField(default='')
	grouping_columns = models.TextField(default='')

	def __str__(self):
		return self.plot_name

	@classmethod
	def create(cls, user):
		plots_count = Plot.objects.filter(user__id = user.id).count()

		new_plot = Plot.objects.create(plot_name='New Plot #' + str(plots_count + 1), user=user)

		return new_plot

	def chart(self):
		data_column_str = self.data_columns.replace("'", "")
		grouping_column_str = self.grouping_columns.replace("'", "")

		data_columns = []
		grouping_columns = []
		if len(data_column_str) > 0:
			data_columns = [int(i) for i in data_column_str.split(', ')]

		if len(grouping_column_str) > 0:
			grouping_columns = [int(i) for i in grouping_column_str.split(', ')]

		actual_plot = None
		if self.plot_type == 'B':
			actual_plot = BarChart(explicit_size = True)
		elif self.plot_type == 'L':
			actual_plot = LineChart(explicit_size = True)
		elif self.plot_type == 'R':
			actual_plot = RadarChart(explicit_size = True)
		elif self.plot_type == 'P':
			actual_plot = PieChart(explicit_size = True)
		elif self.plot_type == 'X':
			actual_plot = BoxChart(explicit_size = True)
		else: # elif self.plot_type == 'X':
			actual_plot = PyramidChart(explicit_size = True)

		columns = Column.objects.filter(spreadsheet=self.spreadsheet)
		actual_plot.set_data(columns.filter(id__in=data_columns))
		actual_plot.height = 600
		actual_plot.width = 800

		return actual_plot.generate()

# class PlotData(models.Model):
# 	PLOTDATA_TYPES = (
# 		('D', 'DataColumn'),
# 		('G', 'GroupingColumn'),
# 	)

# 	plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
# 	column = models.ForeignKey(Column, on_delete=models.CASCADE)
# 	plot_type = models.CharField(max_length=1, choices=PLOTDATA_TYPES, default='D')

class Report(models.Model):
	user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
	report_name = models.CharField(max_length=255)
	report_description = models.TextField(default='')

	report_creation_date = models.DateField(auto_now_add=True, editable=False)
	report_last_modification = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.report_name

	@classmethod
	def create(cls, user):
		reports_count = Report.objects.filter(user__id = user.id).count()

		new_report = Report.objects.create(report_name='New Report #' + str(reports_count + 1), user=user)

		return new_report

class ReportElement(models.Model):
	report = models.ForeignKey(Report, related_name='reportElements', on_delete=models.CASCADE)
	
	ELEMENT_TYPE = (
		('X', 'Text Block'),
		('T', 'Table'),
		('P', 'Plot'),
		('R', 'Report'),
	)

	element_name = models.CharField(max_length=255)
	element_order = models.IntegerField()
	element_type = models.CharField(max_length=1, choices=ELEMENT_TYPE, default='X')

	# ==== Text ====
	text = models.TextField()

	# ==== Table & plot common ====
	caption = models.CharField(max_length=255)
	spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, null=True, blank=True)

	# ==== Table ====
	TABLE_STYLE = (
		('C', 'Classic'),
		('M', 'Modern'),
		('O', 'Office'),
		('A', 'Alternating'),
	)

	style = models.CharField(max_length=1, choices=TABLE_STYLE, default='C')

	# ==== Plot ====
	plot = models.ForeignKey(Plot, on_delete=models.CASCADE, blank=True, null=True)

	# ==== Report ====
	embedded_raport = models.ForeignKey(Report, related_name='reportEmbedded', on_delete=models.CASCADE, blank=True, null=True)
	element_start = models.IntegerField(blank=True, null=True)
	element_end = models.IntegerField(blank=True, null=True)


# class ReportElementText(models.Model):
# 	report = models.ForeignKey(Report, on_delete=models.CASCADE)
# 	element_name = models.CharField(max_length=255)
# 	text = models.TextField()
# 	order = models.IntegerField()

# class ReportElementTable(models.Model):
# 	TABLE_STYLE = (
# 		('C', 'Classic'),
# 		('M', 'Modern'),
# 		('O', 'Office'),
# 		('A', 'Alternating'),
# 	)

# 	report = models.ForeignKey(Report, on_delete=models.CASCADE)
# 	table_caption = models.CharField(max_length=255)
# 	style = models.CharField(max_length=1, choices=TABLE_STYLE, default='C')
# 	rows_columns_inverted = models.BooleanField(default=False)
# 	order = models.IntegerField()

# class ReportElementTableData(models.Model):
# 	report = models.ForeignKey(ReportElementTable, on_delete=models.CASCADE)
# 	column = models.ForeignKey(Column, on_delete=models.CASCADE)
# 	order = models.IntegerField()

# class ReportElementPlot(models.Model):
# 	report = models.ForeignKey(Report, on_delete=models.CASCADE)
# 	plot_caption = models.CharField(max_length=255)
# 	plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
# 	order = models.IntegerField()

# class ReportElementReport(models.Model):
# 	report = models.ForeignKey(Report, related_name='report', on_delete=models.CASCADE)
# 	embedded_raport_caption = models.CharField(max_length=255)
# 	embedded_raport = models.ForeignKey(Report, related_name='reportEmbedded', on_delete=models.CASCADE)
# 	element_start = models.IntegerField()
# 	element_end = models.IntegerField()
# 	order = models.IntegerField()
