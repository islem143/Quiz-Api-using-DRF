from decimal import Clamped
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin, BaseUserManager
from django.db.models import indexes
from django.db.models.fields import CharField
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, user_name, full_name, password, **other_feilds):

        other_feilds.setdefault("is_staff", True)
        other_feilds.setdefault("is_active", True)
        other_feilds.setdefault("is_superuser", True)

        return self.create_user(email, user_name, full_name, password, **other_feilds)

    def create_user(self, email, user_name, full_name, password, **other_feilds):
 
        if not email:
            raise ValueError('Users must have an email address')
        if not user_name:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          full_name=full_name, **other_feilds)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255,blank=True)
    created = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects=CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['user_name','full_name']
    # class Meta:
    #     indexes=[
    #         models.Index(fields=['email'])
    #     ]
    
    def __str__(self) -> str:
        return f'{self.user_name}'


class Teacher(User):
    grade=CharField(max_length=255,default="b")
    pass


class Student(User):

    pass
