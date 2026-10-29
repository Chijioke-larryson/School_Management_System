from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ["admission_number", "first_name", "last_name", "school_class", "gender"]
	list_filter = ["school_class", "gender"]
	search_fields = ["admission_number", "first_name", "last_name"]
