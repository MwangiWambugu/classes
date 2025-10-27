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
    from authentication.models import InstructorFollow

    # Get instructors that the user is following
    following_instructor_ids = InstructorFollow.objects.filter(
        student=request.user
    ).values_list('instructor_id', flat=True)

    # Get courses based on following status
    # Show courses from followed instructors OR courses available through search
    search_query = request.GET.get('search', '')

    if search_query:
        # When searching, show all published courses matching the query
        courses = Course.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(instructor__username__icontains=search_query) |
            Q(instructor__first_name__icontains=search_query) |
            Q(instructor__last_name__icontains=search_query),
            is_published=True
        ).select_related('category', 'instructor').distinct()
    else:
        # Without search, only show courses from followed instructors
        # If not following anyone, show empty or a message
        if following_instructor_ids:
            courses = Course.objects.filter(
                instructor_id__in=following_instructor_ids,
                is_published=True
            ).select_related('category', 'instructor')
        else:
            courses = Course.objects.none()  # No courses if not following anyone

    # Get user's enrollments
    enrolled_course_ids = Enrollment.objects.filter(
        user=request.user, is_active=True
    ).values_list('course_id', flat=True)

    # Category filter
    category_slug = request.GET.get('category', '')
    categories = Category.objects.all()
    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    # Difficulty filter
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    # Get followed instructors for sidebar/display
    followed_instructors = User.objects.filter(id__in=following_instructor_ids)

    context = {
        'courses': courses,
        'categories': categories,
        'enrolled_course_ids': list(enrolled_course_ids),
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'followed_instructors': followed_instructors,
        'following_count': len(following_instructor_ids),
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
    has_instructor_role = hasattr(request.user, 'auth_profile') and request.user.auth_profile.is_instructor()
    has_courses = Course.objects.filter(instructor=request.user).exists()

    if not request.user.is_staff and not has_instructor_role and not has_courses:
        messages.error(request, "You don't have access to the instructor dashboard.")
        return redirect('lessons')

    # Get instructor's courses
    courses = Course.objects.filter(instructor=request.user).annotate(
        enrollment_count=Count('enrollments', filter=Q(enrollments__is_active=True))
    )

    # Get followers count
    from authentication.models import InstructorFollow
    followers_count = InstructorFollow.objects.filter(instructor=request.user).count()

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
        'followers_count': followers_count,
    }
    return render(request, "lessons/instructor_dashboard.html", context)


@login_required(login_url='/authentication/login/')
def admin_dashboard(request):
    """Admin dashboard view"""
    if not (request.user.is_superuser or (hasattr(request.user, 'auth_profile') and request.user.auth_profile.is_admin())):
        messages.error(request, "You don't have access to the admin dashboard.")
        return redirect('lessons')

    # Statistics
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.filter(is_active=True).count()
    total_instructors = User.objects.filter(auth_profile__role='instructor').count()

    recent_users = User.objects.order_by('-date_joined')[:10]
    recent_courses = Course.objects.order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_instructors': total_instructors,
        'recent_users': recent_users,
        'recent_courses': recent_courses,
    }
    return render(request, "lessons/admin_dashboard.html", context)


@login_required(login_url='/authentication/login/')
def staff_dashboard(request):
    """Staff dashboard view"""
    if not (request.user.is_staff or (hasattr(request.user, 'auth_profile') and request.user.auth_profile.is_staff_member())):
        messages.error(request, "You don't have access to the staff dashboard.")
        return redirect('lessons')

    # Statistics
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.filter(is_active=True).count()
    pending_reviews = 0  # Placeholder for future feature

    recent_enrollments = Enrollment.objects.select_related('user', 'course').order_by('-enrolled_at')[:15]

    context = {
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'pending_reviews': pending_reviews,
        'recent_enrollments': recent_enrollments,
    }
    return render(request, "lessons/staff_dashboard.html", context)


@login_required(login_url='/authentication/login/')
def create_course(request):
    """Create a new course"""
    if not (hasattr(request.user, 'auth_profile') and request.user.auth_profile.is_instructor()):
        messages.error(request, "Only instructors can create courses.")
        return redirect('lessons')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        difficulty = request.POST.get('difficulty', 'beginner')
        duration_hours = request.POST.get('duration_hours', 0)
        thumbnail = request.POST.get('thumbnail', '')

        # Validation
        if not title or not description:
            messages.error(request, "Title and description are required.")
            return redirect('create_course')

        # Create course
        course = Course.objects.create(
            title=title,
            description=description,
            instructor=request.user,
            difficulty=difficulty,
            duration_hours=duration_hours,
            thumbnail=thumbnail,
            is_published=False  # Draft by default
        )

        if category_id:
            category = Category.objects.filter(id=category_id).first()
            if category:
                course.category = category
                course.save()

        messages.success(request, f"Course '{title}' created successfully!")
        return redirect('edit_course', slug=course.slug)

    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "lessons/create_course.html", context)


@login_required(login_url='/authentication/login/')
def edit_course(request, slug):
    """Edit an existing course"""
    course = get_object_or_404(Course, slug=slug, instructor=request.user)

    if request.method == 'POST':
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.difficulty = request.POST.get('difficulty', course.difficulty)
        course.duration_hours = request.POST.get('duration_hours', course.duration_hours)
        course.thumbnail = request.POST.get('thumbnail', course.thumbnail)
        course.is_published = request.POST.get('is_published') == 'on'

        category_id = request.POST.get('category')
        if category_id:
            category = Category.objects.filter(id=category_id).first()
            course.category = category

        course.save()
        messages.success(request, "Course updated successfully!")
        return redirect('edit_course', slug=course.slug)

    categories = Category.objects.all()
    lessons = course.lessons.all()

    context = {
        'course': course,
        'categories': categories,
        'lessons': lessons,
    }
    return render(request, "lessons/edit_course.html", context)


@login_required(login_url='/authentication/login/')
def create_lesson(request, course_slug):
    """Create a new lesson for a course"""
    course = get_object_or_404(Course, slug=course_slug, instructor=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        content_type = request.POST.get('content_type', 'text')
        video_url = request.POST.get('video_url', '')
        audio_url = request.POST.get('audio_url', '')
        image_url = request.POST.get('image_url', '')
        duration_minutes = request.POST.get('duration_minutes', 0)
        order = request.POST.get('order', 0)

        if not title:
            messages.error(request, "Lesson title is required.")
            return redirect('create_lesson', course_slug=course_slug)

        lesson = Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            content_type=content_type,
            video_url=video_url,
            audio_url=audio_url,
            image_url=image_url,
            duration_minutes=duration_minutes,
            order=order
        )

        messages.success(request, f"Lesson '{title}' created successfully!")
        return redirect('edit_lesson', course_slug=course_slug, lesson_slug=lesson.slug)

    context = {'course': course}
    return render(request, "lessons/create_lesson.html", context)


@login_required(login_url='/authentication/login/')
def edit_lesson(request, course_slug, lesson_slug):
    """Edit an existing lesson"""
    course = get_object_or_404(Course, slug=course_slug, instructor=request.user)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

    if request.method == 'POST':
        lesson.title = request.POST.get('title', lesson.title)
        lesson.content = request.POST.get('content', lesson.content)
        lesson.content_type = request.POST.get('content_type', lesson.content_type)
        lesson.video_url = request.POST.get('video_url', '')
        lesson.audio_url = request.POST.get('audio_url', '')
        lesson.image_url = request.POST.get('image_url', '')
        lesson.duration_minutes = request.POST.get('duration_minutes', lesson.duration_minutes)
        lesson.order = request.POST.get('order', lesson.order)

        lesson.save()
        messages.success(request, "Lesson updated successfully!")
        return redirect('edit_course', slug=course_slug)

    context = {
        'course': course,
        'lesson': lesson,
    }
    return render(request, "lessons/edit_lesson.html", context)


@login_required(login_url='/authentication/login/')
def delete_lesson(request, course_slug, lesson_slug):
    """Delete a lesson"""
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=course_slug, instructor=request.user)
        lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

        lesson_title = lesson.title
        lesson.delete()

        messages.success(request, f"Lesson '{lesson_title}' deleted successfully!")
        return redirect('edit_course', slug=course_slug)

    return redirect('instructor_dashboard')


@login_required(login_url='/authentication/login/')
def follow_instructor(request, instructor_id):
    """Follow an instructor"""
    if request.method == 'POST':
        from authentication.models import InstructorFollow

        instructor = get_object_or_404(User, id=instructor_id)

        # Check if instructor has instructor role
        if not (hasattr(instructor, 'auth_profile') and instructor.auth_profile.is_instructor()):
            messages.error(request, "This user is not an instructor.")
            return redirect('lessons')

        # Prevent following yourself
        if instructor == request.user:
            messages.error(request, "You cannot follow yourself.")
            return redirect('lessons')

        # Create or get follow relationship
        follow, created = InstructorFollow.objects.get_or_create(
            student=request.user,
            instructor=instructor
        )

        if created:
            messages.success(request, f"You are now following {instructor.username}!")
        else:
            messages.info(request, f"You are already following {instructor.username}.")

        return redirect('instructor_profile', username=instructor.username)

    return redirect('lessons')


@login_required(login_url='/authentication/login/')
def unfollow_instructor(request, instructor_id):
    """Unfollow an instructor"""
    if request.method == 'POST':
        from authentication.models import InstructorFollow

        instructor = get_object_or_404(User, id=instructor_id)

        follow = InstructorFollow.objects.filter(
            student=request.user,
            instructor=instructor
        ).first()

        if follow:
            follow.delete()
            messages.success(request, f"You have unfollowed {instructor.username}.")
        else:
            messages.info(request, f"You are not following {instructor.username}.")

        return redirect('instructor_profile', username=instructor.username)

    return redirect('lessons')


@login_required(login_url='/authentication/login/')
def instructor_profile(request, username):
    """View instructor profile and their courses"""
    instructor = get_object_or_404(User, username=username)

    # Check if user is an instructor
    if not (hasattr(instructor, 'auth_profile') and instructor.auth_profile.is_instructor()):
        messages.error(request, "This user is not an instructor.")
        return redirect('lessons')

    from authentication.models import InstructorFollow

    # Check if current user is following this instructor
    is_following = InstructorFollow.objects.filter(
        student=request.user,
        instructor=instructor
    ).exists()

    # Get instructor's courses
    # If following or own profile, show all; otherwise only published
    if request.user == instructor:
        courses = Course.objects.filter(instructor=instructor)
    elif is_following:
        courses = Course.objects.filter(instructor=instructor, is_published=True)
    else:
        # For non-followers, only show published courses they can search for
        courses = Course.objects.filter(instructor=instructor, is_published=True)

    # Get follower count
    followers_count = InstructorFollow.objects.filter(instructor=instructor).count()

    context = {
        'instructor': instructor,
        'courses': courses,
        'is_following': is_following,
        'followers_count': followers_count,
        'is_own_profile': request.user == instructor,
    }
    return render(request, "lessons/instructor_profile.html", context)


@login_required(login_url='/authentication/login/')
def search_instructors(request):
    """Search for instructors"""
    query = request.GET.get('q', '')

    if query:
        # Search for users with instructor role
        instructors = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query),
            auth_profile__role='instructor'
        ).distinct()
    else:
        # Show all instructors if no query
        instructors = User.objects.filter(auth_profile__role='instructor')

    context = {
        'instructors': instructors,
        'search_query': query,
    }
    return render(request, "lessons/search_instructors.html", context)
