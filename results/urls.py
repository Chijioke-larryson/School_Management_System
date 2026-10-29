from django.urls import path

from . import views

app_name = "results"

urlpatterns = [
    path("", views.results_home, name="results_home"),
    path("assignments/<int:assignment_id>/enter/", views.enter_results, name="enter_results"),
    path("reports/classes/", views.class_report, name="class_report"),
    path("reports/classes/<int:class_id>/", views.result_summary, name="result_summary"),
]
