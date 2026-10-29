from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from academics.models import SchoolClass, Subject
from students.models import Student

from .models import Result


class ResultModelTests(TestCase):
	def setUp(self):
		user = User.objects.create_user(username="result_student", password="password")
		school_class = SchoolClass.objects.create(name="Test Class")
		subject = Subject.objects.create(name="Mathematics", code="TEST-MATH")
		self.student = Student.objects.create(
			user=user,
			first_name="Test",
			last_name="Student",
			admission_number="RESULT-001",
			date_of_birth=date(2012, 1, 1),
			gender="O",
			guardian_name="Guardian",
			guardian_phone="000",
			address="Test address",
			school_class=school_class,
		)
		self.subject = subject

	def test_total_and_grade_are_calculated(self):
		result = Result(
			student=self.student,
			subject=self.subject,
			term="first",
			test_score=30,
			exam_score=45,
		)

		self.assertEqual(result.total, 75)
		self.assertEqual(result.grade, "A")

	def test_scores_above_maximum_are_rejected(self):
		result = Result(
			student=self.student,
			subject=self.subject,
			term="first",
			test_score=41,
			exam_score=20,
		)

		with self.assertRaises(ValidationError):
			result.full_clean()
