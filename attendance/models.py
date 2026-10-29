from django.db import models


class Attendance(models.Model):
	STATUS_CHOICES = [
		("present", "Present"),
		("absent", "Absent"),
		("late", "Late"),
	]

	student = models.ForeignKey(
		"students.Student",
		on_delete=models.CASCADE,
		related_name="attendance_records",
	)
	date = models.DateField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES)

	class Meta:
		ordering = ["-date", "student"]
		constraints = [
			models.UniqueConstraint(
				fields=["student", "date"],
				name="unique_student_attendance_date",
			)
		]

	def __str__(self):
		return f"{self.student} - {self.date} - {self.get_status_display()}"
