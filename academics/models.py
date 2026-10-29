from django.db import models


class SchoolClass(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Subject(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=20, unique=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return f"{self.code} - {self.name}"


class TeachingAssignment(models.Model):
	teacher = models.ForeignKey(
		"teachers.Teacher",
		on_delete=models.CASCADE,
		related_name="teaching_assignments",
	)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
	school_class = models.ForeignKey(
		SchoolClass,
		on_delete=models.CASCADE,
		related_name="teaching_assignments",
	)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=["teacher", "subject", "school_class"],
				name="unique_teaching_assignment",
			)
		]

	def __str__(self):
		return f"{self.teacher} - {self.subject} - {self.school_class}"
