from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.views import role_required

from .forms import StudentForm
from .models import Student


def own_student(request):
	try:
		return request.user.student
	except request.user.student.RelatedObjectDoesNotExist as error:
		raise PermissionDenied from error


@role_required("admin")
def student_list(request):
	query = request.GET.get("q", "").strip()
	students = Student.objects.select_related("school_class", "user")
	if query:
		students = students.filter(
			Q(first_name__icontains=query)
			| Q(last_name__icontains=query)
			| Q(admission_number__icontains=query)
		)
	return render(request, "students/student_list.html", {"students": students, "query": query})


@role_required("admin")
def student_create(request):
	form = StudentForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		admission_number = form.cleaned_data["admission_number"]
		if User.objects.filter(username=admission_number).exists():
			form.add_error("admission_number", "A user account already uses this admission number.")
		else:
			with transaction.atomic():
				student_user = User.objects.create_user(
					username=admission_number,
					password=admission_number,
					first_name=form.cleaned_data["first_name"],
					last_name=form.cleaned_data["last_name"],
				)
				student = form.save(commit=False)
				student.user = student_user
				student.save()
			messages.success(
				request,
				f"Student {student} was created. Initial username and password: {admission_number}.",
			)
			return redirect("students:student_list")
	return render(request, "students/student_form.html", {"form": form, "title": "Add student"})


@role_required("admin")
def student_detail(request, id):
	student = get_object_or_404(
		Student.objects.select_related("school_class", "user"),
		id=id,
	)
	return render(request, "students/student_detail.html", {"student": student})


@role_required("admin")
def student_edit(request, id):
	student = get_object_or_404(Student.objects.select_related("user"), id=id)
	form = StudentForm(request.POST or None, instance=student)
	if request.method == "POST" and form.is_valid():
		admission_number = form.cleaned_data["admission_number"]
		if User.objects.exclude(id=student.user_id).filter(username=admission_number).exists():
			form.add_error("admission_number", "A user account already uses this admission number.")
		else:
			student_user = student.user
			student_user.username = admission_number
			student_user.first_name = form.cleaned_data["first_name"]
			student_user.last_name = form.cleaned_data["last_name"]
			student_user.save(update_fields=["username", "first_name", "last_name"])
			form.save()
			messages.success(request, f"Student {student} was updated.")
			return redirect("students:student_detail", id=student.id)
	return render(request, "students/student_form.html", {"form": form, "title": "Edit student"})


@role_required("admin")
@require_POST
def student_delete(request, id):
	student = get_object_or_404(Student, id=id)
	student_name = str(student)
	student_user = student.user
	student.delete()
	student_user.delete()
	messages.success(request, f"Student {student_name} and their login account were deleted.")
	return redirect("students:student_list")


@role_required("student")
def portal_profile(request):
	return render(request, "students/portal_profile.html", {"student": own_student(request)})


@role_required("student")
def portal_attendance(request):
	student = own_student(request)
	records = student.attendance_records.all()
	total_days = records.count()
	attended_days = records.filter(status__in=["present", "late"]).count()
	percentage = round((attended_days / total_days) * 100, 1) if total_days else 0
	return render(
		request,
		"students/portal_attendance.html",
		{
			"student": student,
			"records": records,
			"percentage": percentage,
		},
	)


@role_required("student")
def portal_results(request):
	from results.models import Result

	student = own_student(request)
	term = request.GET.get("term", "first")
	valid_terms = {choice[0] for choice in Result.TERM_CHOICES}
	if term not in valid_terms:
		term = "first"
	results = Result.objects.filter(student=student, term=term).select_related("subject")
	return render(
		request,
		"students/portal_results.html",
		{"student": student, "results": results, "term": term, "term_choices": Result.TERM_CHOICES},
	)
