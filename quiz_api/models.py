
from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.utils import timezone
from rest_framework.reverse import reverse
from users.models import Teacher, Student


class Category(models.Model):
    title = models.CharField(max_length=255, default="all")


class Exam(models.Model):
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="teachers", null=True)
    slug = models.SlugField(max_length=250, null=True)
    description = models.CharField(max_length=255, null=True)
    students = models.ManyToManyField(
        Student, through="Student_Exam")

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    title = models.TextField()
    exam = models.ForeignKey(
        Exam, related_name='questions', on_delete=models.CASCADE, null=True)
    # category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    def re(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('quiz_api:question_detail', kwargs={"pk1": self.id, "pk2": self.exam.id})


class Choice(models.Model):
    content = models.TextField()
    is_valid = models.BooleanField()
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE)

    def as_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "is_valid": self.is_valid,
            "question": self.question.get_absolute_url()
        }


class Student_Exam(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    date_taken = models.TimeField(default=timezone.now)
    time_taken = models.TimeField()
    score = models.FloatField()
    choices = models.ManyToManyField(Choice, through="Student_Exam_Choices")


class Student_Exam_Choices(models.Model):
    student_exam = models.ForeignKey(
        Student_Exam, on_delete=models.CASCADE)
    #exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('student_exam', 'choice', 'question')
