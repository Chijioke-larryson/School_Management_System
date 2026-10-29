from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
	list_display = ["student", "subject", "term", "test_score", "exam_score", "total", "grade"]
	list_filter = ["subject", "term"]
	search_fields = ["student__first_name", "student__last_name", "student__admission_number"]
