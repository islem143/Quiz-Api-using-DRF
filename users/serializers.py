from django.contrib.auth import login, models
from rest_framework import serializers
from .models import User, Teacher, Student
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'user_name', 'full_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user = self.Meta.model(**data)
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        password = validated_data["password"]
        instance = self.Meta.model(**validated_data)
        if(password is not None):
            instance.set_password(password)
        instance.save()
        return instance


class TeacherSerializer(UserSerializer):
    
    def create(self, validated_data):
         user=super().create(validated_data)
         teachers=models.Group.objects.get(name="teachers")
         teachers.user_set.add(user)
         return user

    class Meta:
        model = Teacher
        fields = ('id','email', 'user_name', 'full_name', 'password', 'grade')
        extra_kwargs = {'password': {'write_only': True}}

class StudentSerializer(UserSerializer):

    def create(self, validated_data):
         user=super().create(validated_data)
         students=models.Group.objects.get(name="students")
         students.user_set.add(user)
         return user
    class Meta:
        model = Student
        fields = ('id','email', 'user_name', 'full_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}
