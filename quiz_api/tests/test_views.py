from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from quiz_api.models import Exam, Student, Teacher


class TeacherTests(APITestCase):

    def test_list_teachers(self):
        url = reverse("quiz_api:teacher_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_teacher(self):
        url = reverse("quiz_api:teacher_list")
        data = {"name": "test", "email": "test@test.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(Teacher.objects.get().name, 'test')

    def test_create_teacher_invalid_data(self):
        url = reverse("quiz_api:teacher_list")
        data = {"name": "test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Teacher.objects.count(), 0)
