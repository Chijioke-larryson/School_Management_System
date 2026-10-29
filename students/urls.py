from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("add/", views.student_create, name="student_create"),
    path("<int:id>/", views.student_detail, name="student_detail"),
    path("<int:id>/edit/", views.student_edit, name="student_edit"),
    path("<int:id>/delete/", views.student_delete, name="student_delete"),
    path("portal/profile/", views.portal_profile, name="portal_profile"),
    path("portal/attendance/", views.portal_attendance, name="portal_attendance"),
    path("portal/results/", views.portal_results, name="portal_results"),
]
