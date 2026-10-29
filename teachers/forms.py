from django import forms

from academics.models import TeachingAssignment

from .models import Teacher


class TeacherForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    staff_id = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30, required=False)


class TeachingAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeachingAssignment
        fields = ["teacher", "subject", "school_class"]
