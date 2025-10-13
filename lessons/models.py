from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg, Count


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_course_count(self):
        return self.courses.filter(is_published=True).count()


class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_taught')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_hours = models.PositiveIntegerField(default=0, help_text='Estimated course duration in hours')
    thumbnail = models.URLField(blank=True, help_text='URL to course thumbnail image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_lesson_count(self):
        return self.lessons.count()

    def get_enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()

    def get_completion_rate(self):
        total = self.enrollments.filter(is_active=True).count()
        if total == 0:
            return 0
        completed = self.enrollments.filter(completed=True).count()
        return round((completed / total) * 100, 1)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    content = models.TextField()
    video_url = models.URLField(blank=True, help_text='YouTube or video URL')
    duration_minutes = models.PositiveIntegerField(default=0, help_text='Lesson duration in minutes')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        unique_together = ['course', 'slug']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_completion_count(self):
        return self.progress_records.filter(completed=True).count()


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    def get_progress_percentage(self):
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            return 0
        completed_lessons = LessonProgress.objects.filter(
            user=self.user,
            lesson__course=self.course,
            completed=True
        ).count()
        return round((completed_lessons / total_lessons) * 100, 1)

    def check_and_mark_complete(self):
        """Check if all lessons are completed and mark enrollment as complete"""
        total = self.course.lessons.count()
        completed = LessonProgress.objects.filter(
            user=self.user,
            lesson__course=self.course,
            completed=True
        ).count()

        if total > 0 and total == completed and not self.completed:
            self.completed = True
            from django.utils import timezone
            self.completed_at = timezone.now()
            self.save()
            return True
        return False


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name_plural = 'Lesson Progress'
        ordering = ['lesson__order']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({'✓' if self.completed else '○'})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True, help_text='Avatar image URL')
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_completed_courses_count(self):
        return Enrollment.objects.filter(user=self.user, completed=True).count()

    def get_in_progress_courses_count(self):
        return Enrollment.objects.filter(user=self.user, completed=False, is_active=True).count()

    def get_total_lessons_completed(self):
        return LessonProgress.objects.filter(user=self.user, completed=True).count()


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    passing_score = models.PositiveIntegerField(default=70, help_text='Passing score percentage')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

    def get_question_count(self):
        return self.questions.count()


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    order = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.text} ({'✓' if self.is_correct else '✗'})"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0)
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_id = models.CharField(max_length=100, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-issued_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Certificate"

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            import uuid
            self.certificate_id = f"CS-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
