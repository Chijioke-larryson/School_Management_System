from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import Profile
from accounts.views import role_required

from academics.models import TeachingAssignment

from .forms import TeacherForm, TeachingAssignmentForm
from .models import Teacher


def teacher_form_for(request, teacher=None):
	initial = None
	if teacher is not None:
		initial = {
			"first_name": teacher.user.first_name,
			"last_name": teacher.user.last_name,
			"email": teacher.user.email,
			"staff_id": teacher.staff_id,
			"phone": teacher.phone,
		}
	return TeacherForm(request.POST or None, initial=initial)


@role_required("admin")
def teacher_list(request):
	teachers = Teacher.objects.select_related("user")
	return render(request, "teachers/teacher_list.html", {"teachers": teachers})


@role_required("admin")
def teacher_create(request):
	form = teacher_form_for(request)
	if request.method == "POST" and form.is_valid():
		staff_id = form.cleaned_data["staff_id"]
		if User.objects.filter(username=staff_id).exists():
			form.add_error("staff_id", "A user account already uses this staff ID.")
		else:
			with transaction.atomic():
				teacher_user = User.objects.create_user(
					username=staff_id,
					password=staff_id,
					first_name=form.cleaned_data["first_name"],
					last_name=form.cleaned_data["last_name"],
					email=form.cleaned_data["email"],
				)
				teacher = Teacher.objects.create(
					user=teacher_user,
					staff_id=staff_id,
					phone=form.cleaned_data["phone"],
				)
				Profile.objects.create(user=teacher_user, role="teacher")
			messages.success(
				request,
				f"Teacher {teacher} was created. Initial username and password: {staff_id}.",
			)
			return redirect("teachers:teacher_list")
	return render(request, "teachers/teacher_form.html", {"form": form, "title": "Add teacher"})


@role_required("admin")
def teacher_edit(request, id):
	teacher = get_object_or_404(Teacher.objects.select_related("user"), id=id)
	form = teacher_form_for(request, teacher)
	if request.method == "POST" and form.is_valid():
		staff_id = form.cleaned_data["staff_id"]
		if User.objects.exclude(id=teacher.user_id).filter(username=staff_id).exists():
			form.add_error("staff_id", "A user account already uses this staff ID.")
		else:
			teacher_user = teacher.user
			teacher_user.username = staff_id
			teacher_user.first_name = form.cleaned_data["first_name"]
			teacher_user.last_name = form.cleaned_data["last_name"]
			teacher_user.email = form.cleaned_data["email"]
			teacher_user.save(update_fields=["username", "first_name", "last_name", "email"])
			teacher.staff_id = staff_id
			teacher.phone = form.cleaned_data["phone"]
			teacher.save(update_fields=["staff_id", "phone"])
			messages.success(request, f"Teacher {teacher} was updated.")
			return redirect("teachers:teacher_list")
	return render(request, "teachers/teacher_form.html", {"form": form, "title": "Edit teacher"})


@role_required("admin")
@require_POST
def teacher_delete(request, id):
	teacher = get_object_or_404(Teacher, id=id)
	teacher_name = str(teacher)
	teacher_user = teacher.user
	teacher.delete()
	teacher_user.delete()
	messages.success(request, f"Teacher {teacher_name} and their login account were deleted.")
	return redirect("teachers:teacher_list")


@role_required("admin")
def assignment_list(request):
	assignments = TeachingAssignment.objects.select_related("teacher__user", "subject", "school_class")
	return render(request, "teachers/assignment_list.html", {"assignments": assignments})


@role_required("admin")
def assignment_create(request):
	form = TeachingAssignmentForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		assignment = form.save()
		messages.success(request, f"Teaching assignment {assignment} was created.")
		return redirect("teachers:assignment_list")
	return render(request, "teachers/assignment_form.html", {"form": form, "title": "Add teaching assignment"})


@role_required("admin")
def assignment_edit(request, id):
	assignment = get_object_or_404(TeachingAssignment, id=id)
	form = TeachingAssignmentForm(request.POST or None, instance=assignment)
	if request.method == "POST" and form.is_valid():
		assignment = form.save()
		messages.success(request, f"Teaching assignment {assignment} was updated.")
		return redirect("teachers:assignment_list")
	return render(request, "teachers/assignment_form.html", {"form": form, "title": "Edit teaching assignment"})


@role_required("admin")
@require_POST
def assignment_delete(request, id):
	assignment = get_object_or_404(TeachingAssignment, id=id)
	assignment_name = str(assignment)
	assignment.delete()
	messages.success(request, f"Teaching assignment {assignment_name} was deleted.")
	return redirect("teachers:assignment_list")
