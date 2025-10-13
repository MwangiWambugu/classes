from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson


@login_required(login_url='/authentication/login/')
def home(request):
    courses = Course.objects.filter(is_published=True)
    context = {
        'courses': courses
    }
    return render(request, "lessons/index.html", context)


@login_required(login_url='/authentication/login/')
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, "lessons/course_detail.html", context)


@login_required(login_url='/authentication/login/')
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    all_lessons = course.lessons.all()

    # Get previous and next lessons
    lesson_list = list(all_lessons)
    current_index = lesson_list.index(lesson)
    previous_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson
    }
    return render(request, "lessons/lesson_detail.html", context)