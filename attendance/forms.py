from django import forms

from .models import Attendance


class AttendanceDateForm(forms.Form):
    attendance_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Attendance date",
    )


class AttendanceEntryForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput)
    status = forms.ChoiceField(choices=Attendance.STATUS_CHOICES)
