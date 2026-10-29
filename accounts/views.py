from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from academics.models import SchoolClass, TeachingAssignment
from attendance.models import Attendance
from results.models import Result
from students.models import Student
from teachers.models import Teacher


def home(request):
	"""Display the public home page."""
	return render(request, "accounts/home.html")


def login_view(request):
	if request.user.is_authenticated:
		return redirect("accounts:dashboard")

	form = AuthenticationForm(request, data=request.POST or None)
	if request.method == "POST" and form.is_valid():
		user = form.get_user()
		login(request, user)
		welcome_name = user.get_full_name() or user.username
		request.session["welcome_name"] = welcome_name
		messages.success(request, f"Welcome, {welcome_name}.")
		return redirect("accounts:dashboard")

	return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
	logout(request)
	messages.info(request, "You have been logged out.")
	return redirect("accounts:home")


def role_required(*allowed_roles):
	"""Allow only logged-in users whose Profile role is listed."""
	def decorator(view_function):
		@wraps(view_function)
		@login_required(login_url="accounts:login")
		def wrapped_view(request, *args, **kwargs):
			if request.user.is_superuser:
				role = "admin"
			else:
				try:
					role = request.user.profile.role
				except request.user.profile.RelatedObjectDoesNotExist as error:
					raise PermissionDenied from error

			if role not in allowed_roles:
				raise PermissionDenied
			return view_function(request, *args, **kwargs)

		return wrapped_view

	return decorator


@login_required(login_url="accounts:login")
def dashboard(request):
	if request.user.is_superuser:
		role = "admin"
	else:
		try:
			role = request.user.profile.role
		except request.user.profile.RelatedObjectDoesNotExist as error:
			raise PermissionDenied from error

	context = {"role": role}
	if role == "admin":
		context.update(
			{
				"student_count": Student.objects.count(),
				"teacher_count": Teacher.objects.count(),
				"class_count": SchoolClass.objects.count(),
				"today_attendance_count": Attendance.objects.filter(
					date=timezone.localdate()
				).count(),
			}
		)
	elif role == "teacher":
		context["assignments"] = TeachingAssignment.objects.filter(
			teacher__user=request.user
		).select_related("school_class", "subject")
	elif role == "student":
		try:
			student = request.user.student
		except request.user.student.RelatedObjectDoesNotExist as error:
			raise PermissionDenied from error
		attendance_records = student.attendance_records.all()
		total_days = attendance_records.count()
		attended_days = attendance_records.filter(status__in=["present", "late"]).count()
		context.update(
			{
				"student": student,
				"attendance_percentage": round((attended_days / total_days) * 100, 1)
				if total_days
				else 0,
				"latest_results": Result.objects.filter(student=student)
				.select_related("subject")
				.order_by("-id")[:5],
			}
		)

	dashboard_templates = {
		"admin": "accounts/admin_dashboard.html",
		"teacher": "accounts/teacher_dashboard.html",
		"student": "accounts/student_dashboard.html",
	}
	dashboard_template = dashboard_templates.get(role)
	if dashboard_template is None:
		raise PermissionDenied
	return render(request, dashboard_template, context)
