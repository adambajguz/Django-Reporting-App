from django import forms
from .models import Plot, Spreadsheet

class SpreadsheetForm(forms.Form):
    spreadsheet_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Spreadsheet name'}))
    spreadsheet_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Spreadsheet description', 'rows':4}))

class PlotForm(forms.Form):
    plot_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Plot name'}))
    plot_type = forms.ChoiceField(choices=Plot.PLOT_TYPES)
    spreadsheet = forms.ChoiceField()
    columns = forms.Select()
    
    def __init__(self, user, *args, **kwargs):
        super(PlotForm, self).__init__(*args, **kwargs)
        self.fields['spreadsheet'] = forms.ModelChoiceField(queryset=Spreadsheet.objects.filter(user=user.id))

class ReportForm(forms.Form):
    plot_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Report name'}))


class ReportElementForm(forms.Form):
    element_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Element name'}))
    plot_type = forms.ChoiceField(choices=Plot.PLOT_TYPES)
    spreadsheet = forms.ChoiceField()
    columns = forms.Select()
    
    def __init__(self, user, *args, **kwargs):
        super(PlotForm, self).__init__(*args, **kwargs)
        self.fields['spreadsheet'] = forms.ModelChoiceField(queryset=Spreadsheet.objects.filter(user=user.id))
