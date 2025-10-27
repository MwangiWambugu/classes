from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import (
    Category, Course, Lesson, Enrollment, LessonProgress,
    UserProfile, Quiz, Question, Answer, QuizAttempt, Certificate
)


@login_required(login_url='/authentication/login/')
def home(request):
    # Get all published courses
    courses = Course.objects.filter(is_published=True).select_related('category', 'instructor')

    # Get user's enrollments
    enrolled_course_ids = Enrollment.objects.filter(
        user=request.user, is_active=True
    ).values_list('course_id', flat=True)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    categories = Category.objects.all()
    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    # Difficulty filter
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    context = {
        'courses': courses,
        'categories': categories,
        'enrolled_course_ids': list(enrolled_course_ids),
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
    }
    return render(request, "lessons/index.html", context)


@login_required(login_url='/authentication/login/')
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()

    # Check if user is enrolled
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    is_enrolled = enrollment is not None and enrollment.is_active

    # Get progress if enrolled
    progress_percentage = 0
    if enrollment:
        progress_percentage = enrollment.get_progress_percentage()

    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'progress_percentage': progress_percentage,
    }
    return render(request, "lessons/course_detail.html", context)


@login_required(login_url='/authentication/login/')
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)

    # Check if already enrolled
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'is_active': True}
    )

    if created:
        messages.success(request, f"You've successfully enrolled in {course.title}!")
    else:
        if not enrollment.is_active:
            enrollment.is_active = True
            enrollment.save()
            messages.success(request, f"Welcome back! You've re-enrolled in {course.title}!")
        else:
            messages.info(request, "You're already enrolled in this course.")

    return redirect('course_detail', slug=slug)


@login_required(login_url='/authentication/login/')
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

    # Check if user is enrolled
    enrollment = Enrollment.objects.filter(user=request.user, course=course, is_active=True).first()
    if not enrollment:
        messages.warning(request, "Please enroll in this course to access lessons.")
        return redirect('course_detail', slug=course_slug)

    # Track lesson access and progress
    lesson_progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    # Get all lessons for navigation
    all_lessons = course.lessons.all()
    lesson_list = list(all_lessons)
    current_index = lesson_list.index(lesson)
    previous_lesson = lesson_list[current_index - 1] if current_index > 0 else None
    next_lesson = lesson_list[current_index + 1] if current_index < len(lesson_list) - 1 else None

    # Get quizzes for this lesson
    quizzes = lesson.quizzes.all()

    # Get lesson progress for all lessons in course
    user_progress = LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course
    ).values_list('lesson_id', 'completed')
    progress_dict = dict(user_progress)

    context = {
        'course': course,
        'lesson': lesson,
        'all_lessons': all_lessons,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'lesson_progress': lesson_progress,
        'quizzes': quizzes,
        'progress_dict': progress_dict,
        'enrollment': enrollment,
    }
    return render(request, "lessons/lesson_detail.html", context)


@login_required(login_url='/authentication/login/')
def mark_lesson_complete(request, course_slug, lesson_slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

        # Get or create progress
        progress, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.save()

            # Check if course is complete
            enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
            if enrollment and enrollment.check_and_mark_complete():
                # Generate certificate
                Certificate.objects.get_or_create(
                    user=request.user,
                    course=course
                )
                messages.success(request, f"🎉 Congratulations! You've completed {course.title}! Your certificate is ready.")
            else:
                messages.success(request, f"✓ Lesson marked as complete!")

        return JsonResponse({'success': True, 'completed': True})

    return JsonResponse({'success': False}, status=400)


@login_required(login_url='/authentication/login/')
def user_profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Get enrollments
    enrollments = Enrollment.objects.filter(user=user, is_active=True).select_related('course')
    in_progress = enrollments.filter(completed=False)
    completed = enrollments.filter(completed=True)

    # Get certificates
    certificates = Certificate.objects.filter(user=user).select_related('course')

    # Statistics
    stats = {
        'total_enrolled': enrollments.count(),
        'in_progress': in_progress.count(),
        'completed': completed.count(),
        'lessons_completed': LessonProgress.objects.filter(user=user, completed=True).count(),
        'quiz_attempts': QuizAttempt.objects.filter(user=user).count(),
    }

    context = {
        'profile_user': user,
        'profile': profile,
        'in_progress_courses': in_progress,
        'completed_courses': completed,
        'certificates': certificates,
        'stats': stats,
        'is_own_profile': request.user == user,
    }
    return render(request, "lessons/profile.html", context)


@login_required(login_url='/authentication/login/')
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.website = request.POST.get('website', '')
        profile.github = request.POST.get('github', '')
        profile.linkedin = request.POST.get('linkedin', '')
        profile.avatar = request.POST.get('avatar', '')
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile', username=request.user.username)

    context = {'profile': profile}
    return render(request, "lessons/edit_profile.html", context)


@login_required(login_url='/authentication/login/')
def my_courses(request):
    enrollments = Enrollment.objects.filter(
        user=request.user, is_active=True
    ).select_related('course').order_by('-enrolled_at')

    context = {'enrollments': enrollments}
    return render(request, "lessons/my_courses.html", context)


@login_required(login_url='/authentication/login/')
def certificate_view(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)

    # Check if user owns this certificate
    if certificate.user != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this certificate.")
        return redirect('lessons')

    context = {'certificate': certificate}
    return render(request, "lessons/certificate.html", context)


@login_required(login_url='/authentication/login/')
def quiz_view(request, course_slug, lesson_slug, quiz_id):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)
    quiz = get_object_or_404(Quiz, id=quiz_id, lesson=lesson)

    # Check enrollment
    enrollment = Enrollment.objects.filter(user=request.user, course=course, is_active=True).first()
    if not enrollment:
        messages.warning(request, "Please enroll in this course to take quizzes.")
        return redirect('course_detail', slug=course_slug)

    questions = quiz.questions.prefetch_related('answers').all()

    context = {
        'course': course,
        'lesson': lesson,
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, "lessons/quiz.html", context)


@login_required(login_url='/authentication/login/')
def quiz_submit(request, course_slug, lesson_slug, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()

        total_points = sum(q.points for q in questions)
        earned_points = 0

        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                answer = Answer.objects.filter(id=selected_answer_id, question=question).first()
                if answer and answer.is_correct:
                    earned_points += question.points

        score = (earned_points / total_points * 100) if total_points > 0 else 0
        passed = score >= quiz.passing_score

        # Save attempt
        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            passed=passed
        )

        if passed:
            messages.success(request, f"🎉 Congratulations! You passed with {score:.1f}%")
        else:
            messages.warning(request, f"You scored {score:.1f}%. Passing score is {quiz.passing_score}%. Try again!")

        return redirect('lesson_detail', course_slug=course_slug, lesson_slug=lesson_slug)

    return redirect('lessons')


@login_required(login_url='/authentication/login/')
def instructor_dashboard(request):
    # Check if user is an instructor
    if not request.user.is_staff and not Course.objects.filter(instructor=request.user).exists():
        messages.error(request, "You don't have access to the instructor dashboard.")
        return redirect('lessons')

    # Get instructor's courses
    courses = Course.objects.filter(instructor=request.user).annotate(
        enrollment_count=Count('enrollments', filter=Q(enrollments__is_active=True))
    )

    # Statistics
    total_students = Enrollment.objects.filter(
        course__instructor=request.user,
        is_active=True
    ).values('user').distinct().count()

    total_completions = Enrollment.objects.filter(
        course__instructor=request.user,
        completed=True
    ).count()

    context = {
        'courses': courses,
        'total_courses': courses.count(),
        'total_students': total_students,
        'total_completions': total_completions,
    }
    return render(request, "lessons/instructor_dashboard.html", context)
