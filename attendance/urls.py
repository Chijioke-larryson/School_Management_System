from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_home, name="attendance_home"),
    path("classes/<int:class_id>/mark/", views.mark_attendance, name="mark_attendance"),
    path("students/<int:student_id>/", views.student_attendance_history, name="student_history"),
]
