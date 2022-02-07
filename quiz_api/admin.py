from django.contrib import admin
from .models import Exam,Question,Category,Choice,Student_Exam,Student_Exam_Choices
# Register your models here.




admin.site.register(Exam)
admin.site.register(Category)
admin.site.register(Student_Exam)
admin.site.register(Student_Exam_Choices)
admin.site.register(Choice)
admin.site.register(Question)