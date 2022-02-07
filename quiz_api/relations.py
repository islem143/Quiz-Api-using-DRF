from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Question


class QuestionHyperLink(serializers.HyperlinkedRelatedField):
    view_name = 'quiz_api:question_detail'

    def get_url(self, obj, view_name, request, format):
        url_kwargs={"pk1":obj.exam.id,"pk2":obj.id}
 
        return reverse(view_name,kwargs=url_kwargs,request=request,format=format)
