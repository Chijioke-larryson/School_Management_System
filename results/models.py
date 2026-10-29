from django.db import models
from django.core.exceptions import ValidationError


class Result(models.Model):
	TERM_CHOICES = [
		("first", "First Term"),
		("second", "Second Term"),
		("third", "Third Term"),
	]

	student = models.ForeignKey(
		"students.Student",
		on_delete=models.CASCADE,
		related_name="results",
	)
	subject = models.ForeignKey(
		"academics.Subject",
		on_delete=models.PROTECT,
		related_name="results",
	)
	term = models.CharField(max_length=10, choices=TERM_CHOICES)
	test_score = models.DecimalField(max_digits=5, decimal_places=2)
	exam_score = models.DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		ordering = ["student", "subject", "term"]
		constraints = [
			models.UniqueConstraint(
				fields=["student", "subject", "term"],
				name="unique_student_subject_term_result",
			)
		]

	def clean(self):
		errors = {}
		if self.test_score < 0 or self.test_score > 40:
			errors["test_score"] = "Test score must be between 0 and 40."
		if self.exam_score < 0 or self.exam_score > 60:
			errors["exam_score"] = "Exam score must be between 0 and 60."
		if errors:
			raise ValidationError(errors)

	@property
	def total(self):
		return self.test_score + self.exam_score

	@property
	def grade(self):
		if self.total >= 70:
			return "A"
		if self.total >= 60:
			return "B"
		if self.total >= 50:
			return "C"
		if self.total >= 45:
			return "D"
		return "F"

	def __str__(self):
		return f"{self.student} - {self.subject} - {self.get_term_display()}"
