from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
	GENDER_CHOICES = [
		("F", "Female"),
		("M", "Male"),
		("O", "Other"),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	admission_number = models.CharField(max_length=30, unique=True)
	date_of_birth = models.DateField()
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	guardian_name = models.CharField(max_length=100)
	guardian_phone = models.CharField(max_length=30)
	address = models.TextField()
	school_class = models.ForeignKey(
		"academics.SchoolClass",
		on_delete=models.PROTECT,
		related_name="students",
	)
	date_admitted = models.DateField(default=timezone.localdate)

	class Meta:
		ordering = ["last_name", "first_name"]

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.admission_number})"
