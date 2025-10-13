from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="lessons"),
    path("course/<slug:slug>/", views.course_detail, name="course_detail"),
    path("course/<slug:course_slug>/lesson/<slug:lesson_slug>/", views.lesson_detail, name="lesson_detail"),
]