from django.contrib import admin
from .models import (
    Category, Course, Lesson, Enrollment, LessonProgress,
    UserProfile, Quiz, Question, Answer, QuizAttempt, Certificate
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_course_count', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'difficulty', 'is_published', 'get_enrolled_count', 'created_at')
    list_filter = ('is_published', 'difficulty', 'category', 'created_at', 'instructor')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Course Details', {
            'fields': ('instructor', 'difficulty', 'duration_hours', 'thumbnail')
        }),
        ('Publication', {
            'fields': ('is_published',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration_minutes', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content', 'course__title')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('course', 'order')
    list_editable = ('order',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'is_active', 'completed', 'get_progress_percentage')
    list_filter = ('is_active', 'completed', 'enrolled_at', 'course')
    search_fields = ('user__username', 'course__title')
    date_hierarchy = 'enrolled_at'
    ordering = ('-enrolled_at',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at', 'last_accessed')
    list_filter = ('completed', 'lesson__course', 'completed_at')
    search_fields = ('user__username', 'lesson__title')
    ordering = ('-last_accessed',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'get_completed_courses_count', 'get_in_progress_courses_count', 'created_at')
    search_fields = ('user__username', 'bio', 'location')
    ordering = ('-created_at',)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    fields = ('text', 'is_correct', 'order')


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'order', 'points')
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'passing_score', 'get_question_count', 'created_at')
    list_filter = ('lesson__course', 'created_at')
    search_fields = ('title', 'description', 'lesson__title')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type', 'order', 'points')
    list_filter = ('question_type', 'quiz__lesson__course')
    search_fields = ('text', 'quiz__title')
    ordering = ('quiz', 'order')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'order')
    list_filter = ('is_correct',)
    search_fields = ('text', 'question__text')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'passed', 'completed_at')
    list_filter = ('passed', 'completed_at', 'quiz__lesson__course')
    search_fields = ('user__username', 'quiz__title')
    date_hierarchy = 'completed_at'
    ordering = ('-completed_at',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'certificate_id', 'issued_at')
    list_filter = ('issued_at', 'course')
    search_fields = ('user__username', 'course__title', 'certificate_id')
    date_hierarchy = 'issued_at'
    ordering = ('-issued_at',)
    readonly_fields = ('certificate_id',)
