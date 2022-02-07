from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.http import JsonResponse

app_name = "users"

urlpatterns = [
    path('register/', views.Register.as_view(), name="register")

]


urlpatterns = format_suffix_patterns(urlpatterns)


