from django import forms
from django.forms import formset_factory

from .models import Result


class TermForm(forms.Form):
    term = forms.ChoiceField(choices=Result.TERM_CHOICES, label="Term")


class ResultEntryForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput)
    test_score = forms.DecimalField(min_value=0, max_value=40, max_digits=5, decimal_places=2)
    exam_score = forms.DecimalField(min_value=0, max_value=60, max_digits=5, decimal_places=2)


ResultEntryFormSet = formset_factory(ResultEntryForm, extra=0)
