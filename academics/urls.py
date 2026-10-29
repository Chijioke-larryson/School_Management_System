from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("classes/", views.class_list, name="class_list"),
    path("classes/add/", views.class_create, name="class_create"),
    path("classes/<int:id>/edit/", views.class_edit, name="class_edit"),
    path("classes/<int:id>/delete/", views.class_delete, name="class_delete"),
    path("subjects/", views.subject_list, name="subject_list"),
    path("subjects/add/", views.subject_create, name="subject_create"),
    path("subjects/<int:id>/edit/", views.subject_edit, name="subject_edit"),
    path("subjects/<int:id>/delete/", views.subject_delete, name="subject_delete"),
]
