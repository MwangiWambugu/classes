from django.urls import path
from . import views


urlpatterns = [
    # Main pages
    path("", views.home, name="lessons"),
    path("my-courses/", views.my_courses, name="my_courses"),

    # Dashboards
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("instructor/dashboard/", views.instructor_dashboard, name="instructor_dashboard"),

    # Course management (instructor)
    path("instructor/course/create/", views.create_course, name="create_course"),
    path("instructor/course/<slug:slug>/edit/", views.edit_course, name="edit_course"),

    # Lesson management (instructor)
    path("instructor/course/<slug:course_slug>/lesson/create/", views.create_lesson, name="create_lesson"),
    path("instructor/course/<slug:course_slug>/lesson/<slug:lesson_slug>/edit/", views.edit_lesson, name="edit_lesson"),
    path("instructor/course/<slug:course_slug>/lesson/<slug:lesson_slug>/delete/", views.delete_lesson, name="delete_lesson"),

    # Instructor profile and following
    path("instructors/", views.search_instructors, name="search_instructors"),
    path("instructor/<str:username>/", views.instructor_profile, name="instructor_profile"),
    path("instructor/<int:instructor_id>/follow/", views.follow_instructor, name="follow_instructor"),
    path("instructor/<int:instructor_id>/unfollow/", views.unfollow_instructor, name="unfollow_instructor"),

    # Course actions
    path("course/<slug:slug>/", views.course_detail, name="course_detail"),
    path("course/<slug:slug>/enroll/", views.enroll_course, name="enroll_course"),

    # Lesson actions
    path("course/<slug:course_slug>/lesson/<slug:lesson_slug>/", views.lesson_detail, name="lesson_detail"),
    path("course/<slug:course_slug>/lesson/<slug:lesson_slug>/complete/", views.mark_lesson_complete, name="mark_lesson_complete"),

    # Quiz
    path("course/<slug:course_slug>/lesson/<slug:lesson_slug>/quiz/<int:quiz_id>/", views.quiz_view, name="quiz_view"),
    path("course/<slug:course_slug>/lesson/<slug:lesson_slug>/quiz/<int:quiz_id>/submit/", views.quiz_submit, name="quiz_submit"),

    # User profile
    path("profile/", views.user_profile, name="my_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),

    # Certificates
    path("certificate/<str:certificate_id>/", views.certificate_view, name="certificate_view"),
]