from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

app_name = "quiz_api"

# router=DefaultRouter()
# router.register('exams',views.ExamList,basename="exam")
# urlpatterns=router.urls
urlpatterns = [
    path("exams/", views.exam_list.as_view(), name="exam_list"),
    path("exams/<int:pk>/", views.exam_detail.as_view(), name="exam_detail"),
    path("exams/<int:pk>/questions/",
         views.questions_list.as_view(), name="question_list"),
    path("exams/<int:pk1>/questions/<int:pk2>/", views.question_detail.as_view(),
         name="question_detail"),
    path("questions/<int:pk>/choices/",
         views.q_choice_list.as_view(), name="question_choice_list"),
    path("questions", views.questions_listT.as_view(), name="question_listT"),
    path("questions/<int:pk>/choices/<int:pk2>/",
         views.choice_detail.as_view(), name="choice_detail"),
    path("choices/",
         views.choice_list.as_view(), name="choice_list"),
    path('categories/', views.category_list.as_view(), name="category_list"),
    path('categories/<int:pk>', views.category_detail.as_view(),
         name="category_detail")


]


urlpatterns = format_suffix_patterns(urlpatterns)
