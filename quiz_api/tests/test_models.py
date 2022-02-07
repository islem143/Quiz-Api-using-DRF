from quiz_api.models import Exam, Student, Teacher
from django.test import TestCase
import datetime


class TestTModels(TestCase):
    def setUp(self) -> None:
        self.teacher = Teacher.objects.create(
            name="test", email="test@test.com")
        self.student = Student.objects.create(
            name="test", email="test@test.com")
        self.exam = Exam.objects.create(
            title="test", duration=datetime.timedelta(hours=1), teacher_id=self.teacher)

    def test_teacher_instance(self):
      
        self.assertTrue(isinstance(self.teacher, Teacher))
        self.assertEqual(str(self.teacher), "test")

    def test_student_instance(self):
        self.assertTrue(isinstance(self.student, Student))
        self.assertEqual(str(self.student), "test")

    def test_exam_instance(self):

        self.assertTrue(isinstance(self.exam, Exam))
        self.assertEqual(str(self.exam), "test")

