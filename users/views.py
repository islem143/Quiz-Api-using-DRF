from .serializers import TeacherSerializer, StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class Register(APIView):

    def post(self, request):
        serializer = None
        print(request.data)
        if(not 'type' in request.data.keys()):
            return Response({"Type": "please provide a type. it must be a student or teacher"}, status=400)
        user_type = request.data["type"]

        if(user_type == "teacher"):
            serializer = TeacherSerializer(data=request.data)
        elif(user_type == "student"):
            serializer = StudentSerializer(data=request.data)
        elif user_type is None:
            return Response({"Type": "Type must be a student or teacher"}, status=400)
   
        if serializer.is_valid():
            
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=400)

