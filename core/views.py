from django.http import JsonResponse
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import StudentSerializer, TeacherSerializer, UserSerializer


class LoginSerializer(TokenObtainPairSerializer):

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     type = None
    #     if(hasattr(user, "teacher")):
    #         type = "teacher"
    #     elif(hasattr(user, "student")):

    #         type = "student"
    #     token["type"] = type

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        serializer = None
        type = None
        if(hasattr(self.user, "teacher")):
            serializer = TeacherSerializer(self.user).data
            type = "teacher"
        elif(hasattr(self.user, "student")):
            serializer = StudentSerializer(self.user).data
            type = "student"
        data['user'] = serializer
        data["type"] = type
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    }, status=404)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer
