
from random import choice
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Exam, Question, Choice


class ExamSerailier(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all(), required=False
    )
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)

    #     return ret

    class Meta:
        model = Exam
        fields = ('id', 'title', 'duration', 'slug',
                  'description', 'teacher', 'questions')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class ChoiceListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
      
        choice_mapping = {choice.id: choice for choice in instance}
        data_mapping = {item['id']: item for item in validated_data}
        ret = []
      
        for choice_id, data in data_mapping.items():
            choice = choice_mapping.get(choice_id, None)
            if choice is None:
                raise ValidationError(
                    {"error": f"choice with id{choice_id} not found"})
            else:

                ret.append(self.child.update(choice, data))
                
        return ret




class ChoiceSerializer(serializers.ModelSerializer):
    question= serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    id = serializers.IntegerField(required=False)

    # def update(self,instance,validated_data):
    #     print(validated_data.get("content"))
    #     instance.content=validated_data.get("content")
    #     return instance
        
    class Meta:
        model = Choice
        fields = ('id','content','is_valid',"question")
        list_serializer_class = ChoiceListSerializer





class QuestionSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    # choices= serializers.HyperlinkedRelatedField(
    #    queryset=Choice.objects.all(),many=True,view_name="quiz_api:question_choice_list")
    # category = serializers.HyperlinkedRelatedField(
    #   read_only=True,view_name='quiz_api:category_detail')
    exam = serializers.PrimaryKeyRelatedField(
        read_only=True)
    #choices = ChoiceSerializer(read_only=True)
    choices=ChoiceSerializer(many=True,read_only=True)
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     question_id=instance.id
    #     requset = self.context["request"]
    #     exam_id = self.context["exam_id"]

    #     category_url = reverse('quiz_api:category_detail', kwargs={
    #                       "pk": ret["exam"]}, request=requset)
    #     exam_url = reverse('quiz_api:exam_detail', kwargs={
    #                        "pk": ret["category"]}, request=requset)
    #     question_url=reverse('quiz_api:question_detail',
    #     kwargs={"pk1":exam_id,"pk2":question_id},
    #     request=requset
    #     )

    #     # #ret["exam"] = exam_url
    #     # #ret["category"] = category_url

    #     choices=Choice.objects.filter(question=question_id).only('content')
    #     converted_choices=[]
    #     for choice in choices:
    #          choice=choice.as_dict()
    #          choice["question"]=question_url
    #          converted_choices.append(choice)

    #     ret["choices"]=converted_choices
    #     return ret
    # def create(self, validated_data):
      
    #     question = Question(title=validated_data.get(
    #         "title"), exam=validated_data.get("exam"))
    #     question.save()
    #     # choices = validated_data.get("choices")
    #     # arr = []
    #     # print(choices)
    #     # for i in range(len(choices)):
    #     #     arr.append(Choice(
    #     #         content=choices[i]["content"], is_valid=choices[i]["is_valid"], question=question))
    #     # Choice.objects.bulk_create(arr)
    #     return question

    # def update(self, instance, validated_data):
        
    #     print(instance)
    #     # question = Question(title=validated_data.get(
    #     #     "title"), exam=validated_data.get("exam"))
    #     # instance.title = validated_data.get("title")
    #     # choices = validated_data.pop("choices")
    #     # arr = []
        
    #     # for i in range(len(choices)):

    #     #     arr.append(Choice(id=choices[i]["id"], content=choices[i]
    #     #                ["content"], is_valid=choices[i]["is_valid"], question=question))

    #     # Choice.objects.bulk_update(arr, ["content", "is_valid"])

    #     # instance.save()
    #     return instance

    class Meta:
        model = Question
        fields = ('id', 'title', 'exam', 'choices')
       # list_serializer_class = QuestionListSerializer
