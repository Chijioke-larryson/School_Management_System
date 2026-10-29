from django.urls import path

from . import views

app_name = "teachers"

urlpatterns = [
    path("", views.teacher_list, name="teacher_list"),
    path("add/", views.teacher_create, name="teacher_create"),
    path("<int:id>/edit/", views.teacher_edit, name="teacher_edit"),
    path("<int:id>/delete/", views.teacher_delete, name="teacher_delete"),
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("assignments/add/", views.assignment_create, name="assignment_create"),
    path("assignments/<int:id>/edit/", views.assignment_edit, name="assignment_edit"),
    path("assignments/<int:id>/delete/", views.assignment_delete, name="assignment_delete"),
]
