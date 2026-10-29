from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ["user"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_admitted": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }
