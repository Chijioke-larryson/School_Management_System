from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")
	staff_id = models.CharField(max_length=30, unique=True)
	phone = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return f"{self.user.get_full_name()} ({self.staff_id})"
