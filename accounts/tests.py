from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from academics.models import SchoolClass
from students.models import Student

from .models import Profile


class RoleAccessTests(TestCase):
	def setUp(self):
		self.teacher_user = User.objects.create_user(username="teacher", password="password")
		Profile.objects.create(user=self.teacher_user, role="teacher")
		self.student_user = User.objects.create_user(username="student", password="password")
		Profile.objects.create(user=self.student_user, role="student")
		school_class = SchoolClass.objects.create(name="Role Test Class")
		Student.objects.create(
			user=self.student_user,
			first_name="Role",
			last_name="Student",
			admission_number="ROLE-001",
			date_of_birth=date(2012, 1, 1),
			gender="O",
			guardian_name="Guardian",
			guardian_phone="000",
			address="Test address",
			school_class=school_class,
		)

	def test_anonymous_user_is_redirected_to_login(self):
		response = self.client.get(reverse("academics:class_list"))

		self.assertRedirects(response, f"{reverse('accounts:login')}?next=/academics/classes/")

	def test_teacher_cannot_open_admin_class_management(self):
		self.client.login(username="teacher", password="password")

		response = self.client.get(reverse("academics:class_list"))

		self.assertEqual(response.status_code, 403)

	def test_student_portal_uses_logged_in_student(self):
		self.client.login(username="student", password="password")

		response = self.client.get(reverse("students:portal_profile"))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "ROLE-001")
