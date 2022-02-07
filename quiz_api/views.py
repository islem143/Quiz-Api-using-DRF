from django.http.response import Http404

from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response

from rest_framework import generics

from rest_framework.views import APIView
from .serializers import CategorySerializer, ChoiceSerializer, ExamSerailier, QuestionSerializer
from .models import Category, Choice, Exam, Question


class exam_list(APIView):

    def get(self, request):
        exams = Exam.objects.all().prefetch_related("questions")
        ser = ExamSerailier(exams, many=True)
        return Response(ser.data, status=200)

    def post(self, request):

        ser = ExamSerailier(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)

        return Response(ser.errors, status=400)


class exam_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerailier


class questions_listT(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        exam = self.request.query_params.get('exam')

        if exam is not None:
            queryset = Question.objects.filter(exam=exam)
            if len(queryset) == 0:
                raise Http404
        return queryset


class questions_list(APIView):

    def get_exam(self, pk):
        try:

            exam = Exam.objects.get(pk=pk)
            return exam
        except Exam.DoesNotExist:
            raise Http404

    def get(self, request, pk):

        exam = self.get_exam(pk)
        questions = exam.questions.all()
        questions = Question.objects.filter(
            exam=exam).prefetch_related('choices')
        serialzer = QuestionSerializer(
            questions, many=True, context={'request': request, "exam_id": exam.id})

        return Response(serialzer.data, status=200)

    def post(self, requset, pk):
        exam = self.get_exam(pk)
        qusetion = requset.data["question"]
        choices = requset.data["choices"]

        serializer = QuestionSerializer(data=qusetion)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save(exam=exam)
        for c in choices:
            c["question"] = serializer.data["id"]
        choiceSerializer = ChoiceSerializer(data=choices, many=True)
        if not choiceSerializer.is_valid():

            return Response(choiceSerializer.errors, status=400)

        choiceSerializer.save()
        return Response({"question": serializer.data, "choices": choiceSerializer.data}, status=200)

    def put(self, request, pk):

        question = request.data["question"]

        question_db = Question.objects.get(id=question["id"])
        choices = request.data["choices"]

        choices_ids = [c["id"] for c in choices]
        choices_db = Choice.objects.filter(id__in=choices_ids)

        questionSerializer = QuestionSerializer(question_db, data=question)
        if(not questionSerializer.is_valid()):
            return Response(questionSerializer.errors, status=400)

        questionSerializer.save()

        choiceSerializer = ChoiceSerializer(
            choices_db, data=choices, many=True)

        if not choiceSerializer.is_valid():
            return Response(choiceSerializer.errors, status=400)
        choiceSerializer.save()
        return Response({"question": questionSerializer.data, "choices": choiceSerializer.data}, status=200)


class choice_list(APIView):

    def get_queryset(self):
        question_id = self.request.query_params.get('question')
        if(question_id is not None):
            return Choice.objects.filter(question=question_id)
        return Choice.objects.all()

    def get(self, request):

        serializer = ChoiceSerializer(self.get_queryset(), many=True)

        return Response(serializer.data, status=200)

    def post(self, request):
        data = request.data["choices"]
        print(request.data)
        serializer = ChoiceSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class question_detail(APIView):
    def get_exam(self, pk):
        try:

            exam = Exam.objects.get(pk=pk)
            return exam
        except Exam.DoesNotExist:
            raise Http404

    def get(self, request, pk1, pk2=2):

        exam = self.get_exam(pk1)

        question = exam.questions.filter(pk=pk2).first()
        if(question is None):
            return Response({"error": "question not found"}, status=404)
        serialzer = QuestionSerializer(
            question, context={'request': request, "exam_id": exam.id})

        return Response(serialzer.data, status=200)


class category_list(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class category_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class q_choice_list(generics.ListCreateAPIView):

    def get_queryset(self):
        question = self.kwargs["pk"]
        choices = Choice.objects.filter(question=question)
        if len(choices) == 0:
            raise Http404

        return Choice.objects.filter(question=question)

    serializer_class = ChoiceSerializer


class choice_detail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        question = self.kwargs["pk"]
        pk2 = self.kwargs["pk2"]
        return Choice.objects.filter(question=question, pk=pk2)
