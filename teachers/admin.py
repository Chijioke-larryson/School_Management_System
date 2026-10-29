from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
	list_display = ["staff_id", "user", "phone"]
	search_fields = ["staff_id", "user__first_name", "user__last_name"]
