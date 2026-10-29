from django.contrib import admin
from .models import SchoolClass, Subject, TeachingAssignment


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
	list_display = ["name", "description"]
	search_fields = ["name"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
	list_display = ["name", "code"]
	search_fields = ["name", "code"]


@admin.register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
	list_display = ["teacher", "subject", "school_class"]
	list_filter = ["subject", "school_class"]
