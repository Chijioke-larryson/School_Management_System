from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from academics.models import SchoolClass
from accounts.views import role_required
from students.models import Student
from teachers.models import Teacher

from .forms import AttendanceDateForm, AttendanceEntryForm
from .models import Attendance

AttendanceEntryFormSet = formset_factory(AttendanceEntryForm, extra=0)


def teacher_classes(request):
	try:
		teacher = request.user.teacher
	except request.user.teacher.RelatedObjectDoesNotExist as error:
		raise PermissionDenied from error
	return SchoolClass.objects.filter(
		teaching_assignments__teacher=teacher,
	).distinct()


@role_required("teacher")
def attendance_home(request):
	classes = teacher_classes(request)
	return render(request, "attendance/home.html", {"classes": classes})


@role_required("teacher")
def mark_attendance(request, class_id):
	school_class = get_object_or_404(SchoolClass, id=class_id)
	classes = teacher_classes(request)
	if not classes.filter(id=class_id).exists():
		raise PermissionDenied

	students = list(Student.objects.filter(school_class=school_class).order_by("last_name", "first_name"))
	error_message = None
	if request.method == "POST":
		date_form = AttendanceDateForm(request.POST)
		formset = AttendanceEntryFormSet(request.POST)
		if date_form.is_valid() and formset.is_valid():
			attendance_date = date_form.cleaned_data["attendance_date"]
			student_ids = {student.id for student in students}
			submitted_ids = {form.cleaned_data["student_id"] for form in formset}
			if submitted_ids != student_ids:
				error_message = "The student list changed. Please reload and try again."
			elif Attendance.objects.filter(
				student_id__in=student_ids,
				date=attendance_date,
			).exists():
				error_message = "Attendance already exists for at least one student on this date."
			else:
				with transaction.atomic():
					Attendance.objects.bulk_create(
						[
							Attendance(
								student_id=form.cleaned_data["student_id"],
								date=attendance_date,
								status=form.cleaned_data["status"],
							)
							for form in formset
						]
					)
				messages.success(request, f"Attendance for {school_class.name} was saved.")
				return redirect("attendance:attendance_home")
	else:
		attendance_date = timezone.localdate()
		date_form = AttendanceDateForm(initial={"attendance_date": attendance_date})
		formset = AttendanceEntryFormSet(
			initial=[{"student_id": student.id, "status": "present"} for student in students]
		)

	student_forms = zip(students, formset.forms)
	return render(
		request,
		"attendance/mark_attendance.html",
		{
			"school_class": school_class,
			"date_form": date_form,
			"formset": formset,
			"student_forms": student_forms,
			"error_message": error_message,
		},
	)


@role_required("teacher")
def student_attendance_history(request, student_id):
	student = get_object_or_404(Student.objects.select_related("school_class"), id=student_id)
	if not teacher_classes(request).filter(id=student.school_class_id).exists():
		raise PermissionDenied

	records = student.attendance_records.all()
	total_days = records.count()
	attended_days = records.filter(status__in=["present", "late"]).count()
	percentage = round((attended_days / total_days) * 100, 1) if total_days else 0
	return render(
		request,
		"attendance/student_history.html",
		{
			"student": student,
			"records": records,
			"total_days": total_days,
			"attended_days": attended_days,
			"percentage": percentage,
		},
	)
