from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.views import role_required

from .forms import SchoolClassForm, SubjectForm
from .models import SchoolClass, Subject


@role_required("admin")
def class_list(request):
	classes = SchoolClass.objects.all()
	return render(request, "academics/class_list.html", {"classes": classes})


@role_required("admin")
def class_create(request):
	form = SchoolClassForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		school_class = form.save()
		messages.success(request, f"Class {school_class.name} was created.")
		return redirect("academics:class_list")
	return render(request, "academics/class_form.html", {"form": form, "title": "Add class"})


@role_required("admin")
def class_edit(request, id):
	school_class = get_object_or_404(SchoolClass, id=id)
	form = SchoolClassForm(request.POST or None, instance=school_class)
	if request.method == "POST" and form.is_valid():
		form.save()
		messages.success(request, f"Class {school_class.name} was updated.")
		return redirect("academics:class_list")
	return render(request, "academics/class_form.html", {"form": form, "title": "Edit class"})


@role_required("admin")
@require_POST
def class_delete(request, id):
	school_class = get_object_or_404(SchoolClass, id=id)
	class_name = school_class.name
	try:
		school_class.delete()
	except ProtectedError:
		messages.error(request, f"Class {class_name} cannot be deleted while it has students.")
	else:
		messages.success(request, f"Class {class_name} was deleted.")
	return redirect("academics:class_list")


@role_required("admin")
def subject_list(request):
	subjects = Subject.objects.all()
	return render(request, "academics/subject_list.html", {"subjects": subjects})


@role_required("admin")
def subject_create(request):
	form = SubjectForm(request.POST or None)
	if request.method == "POST" and form.is_valid():
		subject = form.save()
		messages.success(request, f"Subject {subject.name} was created.")
		return redirect("academics:subject_list")
	return render(request, "academics/subject_form.html", {"form": form, "title": "Add subject"})


@role_required("admin")
def subject_edit(request, id):
	subject = get_object_or_404(Subject, id=id)
	form = SubjectForm(request.POST or None, instance=subject)
	if request.method == "POST" and form.is_valid():
		form.save()
		messages.success(request, f"Subject {subject.name} was updated.")
		return redirect("academics:subject_list")
	return render(request, "academics/subject_form.html", {"form": form, "title": "Edit subject"})


@role_required("admin")
@require_POST
def subject_delete(request, id):
	subject = get_object_or_404(Subject, id=id)
	subject_name = subject.name
	try:
		subject.delete()
	except ProtectedError:
		messages.error(request, f"Subject {subject_name} cannot be deleted while it is assigned to results.")
	else:
		messages.success(request, f"Subject {subject_name} was deleted.")
	return redirect("academics:subject_list")
