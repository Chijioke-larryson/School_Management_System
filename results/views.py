from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from accounts.views import role_required
from academics.models import SchoolClass, TeachingAssignment
from students.models import Student

from .forms import ResultEntryFormSet, TermForm
from .models import Result


def teacher_assignments(request):
	try:
		teacher = request.user.teacher
	except request.user.teacher.RelatedObjectDoesNotExist as error:
		raise PermissionDenied from error
	return TeachingAssignment.objects.filter(teacher=teacher).select_related(
		"subject",
		"school_class",
	)


def get_teacher_assignment(request, assignment_id):
	assignment = get_object_or_404(
		TeachingAssignment.objects.select_related("teacher__user", "subject", "school_class"),
		id=assignment_id,
	)
	if not teacher_assignments(request).filter(id=assignment.id).exists():
		raise PermissionDenied
	return assignment


@role_required("teacher")
def results_home(request):
	assignments = teacher_assignments(request)
	return render(request, "results/home.html", {"assignments": assignments})


@role_required("teacher")
def enter_results(request, assignment_id):
	assignment = get_teacher_assignment(request, assignment_id)
	students = list(
		Student.objects.filter(school_class=assignment.school_class).order_by("last_name", "first_name")
	)
	selected_term = request.POST.get("term") or request.GET.get("term", "first")
	existing_results = {
		result.student_id: result
		for result in Result.objects.filter(
			student__in=students,
			subject=assignment.subject,
			term=selected_term,
		)
	}

	if request.method == "POST":
		term_form = TermForm(request.POST)
		formset = ResultEntryFormSet(request.POST)
		if term_form.is_valid() and formset.is_valid():
			selected_term = term_form.cleaned_data["term"]
			student_ids = {student.id for student in students}
			submitted_ids = {form.cleaned_data["student_id"] for form in formset}
			if submitted_ids != student_ids:
				formset._non_form_errors = formset.error_class(
					["The student list changed. Please reload and try again."]
				)
			else:
				with transaction.atomic():
					for form in formset:
						result, _ = Result.objects.get_or_create(
							student_id=form.cleaned_data["student_id"],
							subject=assignment.subject,
							term=selected_term,
							defaults={
								"test_score": form.cleaned_data["test_score"],
								"exam_score": form.cleaned_data["exam_score"],
							},
						)
						result.test_score = form.cleaned_data["test_score"]
						result.exam_score = form.cleaned_data["exam_score"]
						result.full_clean()
						result.save()
				messages.success(
					request,
					f"{assignment.subject.name} results for {assignment.school_class.name} were saved.",
				)
				return redirect("results:enter_results", assignment_id=assignment.id)
	else:
		term_form = TermForm(initial={"term": selected_term})
		formset = ResultEntryFormSet(
			initial=[
				{
					"student_id": student.id,
					"test_score": existing_results[student.id].test_score
					if student.id in existing_results
					else 0,
					"exam_score": existing_results[student.id].exam_score
					if student.id in existing_results
					else 0,
				}
				for student in students
			]
		)

	student_forms = zip(students, formset.forms)
	saved_results = Result.objects.filter(
		student__in=students,
		subject=assignment.subject,
		term=selected_term,
	).select_related("student")
	return render(
		request,
		"results/enter_results.html",
		{
			"assignment": assignment,
			"term_form": term_form,
			"formset": formset,
			"student_forms": student_forms,
			"saved_results": saved_results,
			"selected_term": selected_term,
		},
	)


@role_required("admin")
def class_report(request):
	classes = SchoolClass.objects.all()
	return render(request, "results/class_report.html", {"classes": classes})


@role_required("admin")
def result_summary(request, class_id):
	school_class = get_object_or_404(SchoolClass, id=class_id)
	term = request.GET.get("term", "first")
	valid_terms = {choice[0] for choice in Result.TERM_CHOICES}
	if term not in valid_terms:
		term = "first"
	results = Result.objects.filter(
		student__school_class=school_class,
		term=term,
	).select_related("student", "subject")
	return render(
		request,
		"results/result_summary.html",
		{
			"school_class": school_class,
			"results": results,
			"term": term,
			"term_choices": Result.TERM_CHOICES,
		},
	)
