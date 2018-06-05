from django import forms
from django.forms.formsets import BaseFormSet

from reports.models import *

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
    report_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Report name'}))
    report_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Report description', 'rows':4}))


class ReportElementForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    element_name = forms.CharField(required=False, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Element name'}))
    element_order = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': "uk-form-width-small"}))
    element_type = forms.ChoiceField(required=False, choices=ReportElement.ELEMENT_TYPE, widget=forms.Select(attrs={'onchange':'myFunction(event)'}))

    # ==== Text ====
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Text', 'rows':10, 'cols': 75}), required=False)

    # ==== Table & plot common ====
    caption = forms.CharField(required=False, max_length=32, widget=forms.TextInput(attrs={'placeholder': 'Caption'}))

    # ==== Table ====
    style = forms.ChoiceField(required=False, choices=ReportElement.TABLE_STYLE)
    spreadsheet = forms.ChoiceField()

    # ==== Plot ====
    plot = forms.ChoiceField()

    # ==== Report ====
    embedded_raport = forms.ChoiceField(required=False)
    element_start = forms.IntegerField(required=False)
    element_end = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            self.user = user
        super(ReportElementForm, self).__init__(*args, **kwargs)

        self.fields['spreadsheet'] = forms.ModelChoiceField(required=False, queryset=Spreadsheet.objects.filter(user=user.id))
        self.fields['columns'] = forms.ModelChoiceField(required=False, queryset=Report.objects.filter(user=user.id))
        self.fields['plot'] = forms.ModelChoiceField(required=False, queryset=Plot.objects.filter(user=user.id))
        self.fields['embedded_raport'] = forms.ModelChoiceField(required=False, queryset=Report.objects.filter(user=user.id))


# class BaseReportElementFormSet(BaseFormSet):
#     def clean(self):
#         # """
        # Adds validation to check that no two links have the same anchor or URL
        # and that all links have both an anchor and URL.
        # """
        # if any(self.errors):
        #     return

        # anchors = []
        # urls = []
        # duplicates = False

        # for form in self.forms:
        #     if form.cleaned_data:
        #         anchor = form.cleaned_data['anchor']
        #         url = form.cleaned_data['url']

        #         # Check that no two links have the same anchor or URL
        #         if anchor and url:
        #             if anchor in anchors:
        #                 duplicates = True
        #             anchors.append(anchor)

        #             if url in urls:
        #                 duplicates = True
        #             urls.append(url)

        #         if duplicates:
        #             raise forms.ValidationError(
        #                 'Links must have unique anchors and URLs.',
        #                 code='duplicate_links'
        #             )

        #         # Check that all links have both an anchor and URL
        #         if url and not anchor:
        #             raise forms.ValidationError(
        #                 'All links must have an anchor.',
        #                 code='missing_anchor'
        #             )
        #         elif anchor and not url:
        #             raise forms.ValidationError(
        #                 'All links must have a URL.',
        #                 code='missing_URL'
        #             )