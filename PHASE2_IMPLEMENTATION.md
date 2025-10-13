# Phase 2 Implementation Guide

## ✅ Completed So Far

### 1. **Extended Data Models** (lessons/models.py)
- ✅ Category model (course organization)
- ✅ Enhanced Course model (difficulty, duration, thumbnail, category)
- ✅ Enhanced Lesson model (video_url, duration_minutes)
- ✅ Enrollment model (track user course registrations)
- ✅ LessonProgress model (track lesson completion)
- ✅ UserProfile model (bio, avatar, social links)
- ✅ Quiz, Question, Answer models (assessments)
- ✅ QuizAttempt model (track quiz scores)
- ✅ Certificate model (course completion certificates)

### 2. **Django Admin Configuration** (lessons/admin.py)
- ✅ All models registered with comprehensive admin views
- ✅ Inline editing for quizzes and questions
- ✅ Progress tracking displays
- ✅ Enrollment management

### 3. **Views Implementation** (lessons/views.py)
- ✅ Enhanced home() - search, filtering, categories
- ✅ Enhanced course_detail() - enrollment status, progress
- ✅ enroll_course() - course enrollment system
- ✅ Enhanced lesson_detail() - progress tracking, quizzes
- ✅ mark_lesson_complete() - lesson completion API
- ✅ user_profile() - user profiles with statistics
- ✅ edit_profile() - profile editing
- ✅ my_courses() - enrolled courses view
- ✅ certificate_view() - certificate display
- ✅ quiz_view() - quiz taking interface
- ✅ quiz_submit() - quiz grading
- ✅ instructor_dashboard() - instructor analytics

## 🔧 Next Steps to Complete

### Step 1: Update URL Patterns

Edit `lessons/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path("", views.home, name="lessons"),
    path("my-courses/", views.my_courses, name="my_courses"),

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
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # Certificates
    path("certificate/<str:certificate_id>/", views.certificate_view, name="certificate_view"),

    # Instructor
    path("instructor/dashboard/", views.instructor_dashboard, name="instructor_dashboard"),
]
```

### Step 2: Create/Run Migrations

```bash
cd /var/www/html/contract/mwangi_jeremiah/classes
source .venv/bin/activate

# Create migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate
```

### Step 3: Update Existing Templates

The following templates need Phase 2 enhancements:

#### lessons/index.html
- Add search bar
- Add category filter
- Add difficulty filter
- Show enrollment status on cards
- Add "Enroll" button

#### lessons/course_detail.html
- Add enrollment button
- Show progress bar if enrolled
- Display difficulty and duration
- Show "Resume" button for enrolled users
- Add category badge

#### lessons/lesson_detail.html
- Add "Mark as Complete" button
- Show progress indicators
- Display quiz links
- Add completion checkmarks in sidebar
- Show video embed if video_url exists

### Step 4: Create New Templates

#### templates/lessons/profile.html
```html
{% extends "base.html" %}
{% block title %}| {{ profile_user.username}}'s Profile{% endblock %}

{% block content %}
<div class="container-fluid">
  <div class="row">
    <div class="col-md-4">
      <div class="card">
        <div class="card-body text-center">
          {% if profile.avatar %}
            <img src="{{ profile.avatar }}" class="rounded-circle" width="150">
          {% else %}
            <div class="rounded-circle bg-secondary d-inline-block" style="width:150px;height:150px;line-height:150px;">
              <span class="text-white" style="font-size:48px;">{{ profile_user.username.0|upper }}</span>
            </div>
          {% endif %}
          <h3 class="mt-3">{{ profile_user.username }}</h3>
          {% if profile.location %}
            <p class="text-muted"><i class="bi bi-geo-alt"></i> {{ profile.location }}</p>
          {% endif %}
          {% if is_own_profile %}
            <a href="{% url 'edit_profile' %}" class="btn btn-primary">Edit Profile</a>
          {% endif %}
        </div>
      </div>

      <div class="card mt-3">
        <div class="card-body">
          <h5>Statistics</h5>
          <ul class="list-unstyled">
            <li><strong>{{ stats.total_enrolled }}</strong> Courses Enrolled</li>
            <li><strong>{{ stats.completed }}</strong> Courses Completed</li>
            <li><strong>{{ stats.lessons_completed }}</strong> Lessons Completed</li>
            <li><strong>{{ stats.quiz_attempts }}</strong> Quizzes Taken</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="col-md-8">
      {% if profile.bio %}
      <div class="card mb-3">
        <div class="card-body">
          <h5>About</h5>
          <p>{{ profile.bio }}</p>
        </div>
      </div>
      {% endif %}

      <div class="card mb-3">
        <div class="card-header">
          <h5>Courses in Progress ({{ in_progress_courses.count }})</h5>
        </div>
        <div class="list-group list-group-flush">
          {% for enrollment in in_progress_courses %}
          <a href="{% url 'course_detail' enrollment.course.slug %}" class="list-group-item list-group-item-action">
            <div class="d-flex justify-content-between">
              <span>{{ enrollment.course.title }}</span>
              <span class="badge badge-primary">{{ enrollment.get_progress_percentage }}%</span>
            </div>
            <div class="progress mt-2" style="height:5px;">
              <div class="progress-bar" style="width:{{ enrollment.get_progress_percentage }}%"></div>
            </div>
          </a>
          {% empty %}
          <div class="list-group-item">No courses in progress</div>
          {% endfor %}
        </div>
      </div>

      {% if certificates %}
      <div class="card">
        <div class="card-header">
          <h5>Certificates ({{ certificates.count }})</h5>
        </div>
        <div class="list-group list-group-flush">
          {% for cert in certificates %}
          <a href="{% url 'certificate_view' cert.certificate_id %}" class="list-group-item list-group-item-action">
            <i class="bi bi-award text-warning"></i> {{ cert.course.title }}
            <small class="text-muted float-right">{{ cert.issued_at|date:"M d, Y" }}</small>
          </a>
          {% endfor %}
        </div>
      </div>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}
```

#### templates/lessons/certificate.html
```html
{% extends "base.html" %}
{% block title %}| Certificate{% endblock %}

{% block content %}
<div class="container mt-5">
  <div class="row justify-content-center">
    <div class="col-md-10">
      <div class="card border-warning" style="border-width:5px;">
        <div class="card-body text-center py-5">
          <h1 class="display-4 mb-4">Certificate of Completion</h1>
          <h3 class="mb-4">This certifies that</h3>
          <h2 class="text-primary mb-4">{{ certificate.user.get_full_name|default:certificate.user.username }}</h2>
          <h3 class="mb-4">has successfully completed</h3>
          <h2 class="text-success mb-4">{{ certificate.course.title }}</h2>
          <p class="text-muted">Certificate ID: {{ certificate.certificate_id }}</p>
          <p class="text-muted">Issued on: {{ certificate.issued_at|date:"F d, Y" }}</p>
          <hr class="my-4">
          <p class="mb-0">Ctrl+Shift Academy</p>
        </div>
      </div>
      <div class="text-center mt-3">
        <button onclick="window.print()" class="btn btn-primary">Print Certificate</button>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

#### templates/lessons/my_courses.html
```html
{% extends "base.html" %}
{% block title %}| My Courses{% endblock %}

{% block content %}
<div class="container-fluid">
  <h2 class="mb-4">My Enrolled Courses</h2>

  <div class="row">
    {% for enrollment in enrollments %}
    <div class="col-md-4 mb-4">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">{{ enrollment.course.title }}</h5>
          <div class="progress mb-2">
            <div class="progress-bar" style="width:{{ enrollment.get_progress_percentage }}%">
              {{ enrollment.get_progress_percentage }}%
            </div>
          </div>
          <p class="text-muted">Enrolled: {{ enrollment.enrolled_at|date:"M d, Y" }}</p>
          {% if enrollment.completed %}
            <span class="badge badge-success">✓ Completed</span>
          {% endif %}
          <a href="{% url 'course_detail' enrollment.course.slug %}" class="btn btn-primary btn-sm mt-2">
            {% if enrollment.get_progress_percentage > 0 %}Resume{% else %}Start{% endif %}
          </a>
        </div>
      </div>
    </div>
    {% empty %}
    <div class="col-12">
      <div class="alert alert-info">
        You haven't enrolled in any courses yet. <a href="{% url 'lessons' %}">Browse courses</a>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
```

### Step 5: Update Sidebar Navigation

Edit `templates/partials/_sidebar.html`:

```html
{% load static %}
<nav class="col-md-2 d-none d-md-block bg-light sidebar">
  <div class="sidebar-sticky">
    <ul class="nav flex-column">
      <li class="nav-item">
        <a class="nav-link {% if request.path == '/' %}active{% endif %}" href="{% url 'lessons' %}">
          <span data-feather="home"></span>
          Dashboard
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link {% if 'my-courses' in request.path %}active{% endif %}" href="{% url 'my_courses' %}">
          <span data-feather="book-open"></span>
          My Courses
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link {% if 'profile' in request.path %}active{% endif %}" href="{% url 'my_profile' %}">
          <span data-feather="user"></span>
          My Profile
        </a>
      </li>
      {% if user.is_staff or user.courses_taught.exists %}
      <li class="nav-item">
        <a class="nav-link" href="{% url 'instructor_dashboard' %}">
          <span data-feather="bar-chart"></span>
          Instructor Dashboard
        </a>
      </li>
      {% endif %}
      <li class="nav-item">
        <a class="nav-link" href="{% url 'admin:index' %}" target="_blank">
          <span data-feather="settings"></span>
          Admin Panel
        </a>
      </li>
    </ul>
  </div>
</nav>
```

### Step 6: Run Phase 2 Setup

```bash
./setup_phase2.sh
```

Or manually:

```bash
# Activate environment
source .venv/bin/activate

# Migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Seed Phase 2 data
python3 manage.py seed_phase2

# Run server
python3 manage.py runserver
```

## 🎯 Phase 2 Features Summary

### For Students:
1. **Course Enrollment** - One-click enrollment
2. **Progress Tracking** - See completion percentage
3. **Lesson Completion** - Mark lessons as done
4. **Course Certificates** - Auto-generated on completion
5. **User Profiles** - Personal dashboards with stats
6. **Search & Filter** - Find courses by name, category, difficulty
7. **Quizzes** - Test knowledge with assessments
8. **My Courses** - View all enrolled courses

### For Instructors:
1. **Instructor Dashboard** - View student analytics
2. **Course Management** - Enhanced admin interface
3. **Quiz Creation** - Build assessments
4. **Student Tracking** - See who's enrolled and progressing

### System Features:
1. **Category System** - Organize courses by topic
2. **Difficulty Levels** - Beginner, Intermediate, Advanced
3. **Course Duration** - Estimated hours
4. **Video Integration** - Embed video URLs
5. **Social Profiles** - GitHub, LinkedIn links
6. **Certificate System** - Unique certificate IDs

## 📊 Database Relationships

```
Category ─┐
          ├─> Course ─┐
User ─────┤           ├─> Lesson ─┐
          │           │            ├─> Quiz ─> Question ─> Answer
          │           │            │
          │           │            └─> LessonProgress
          │           │
          │           └─> Enrollment
          │
          ├─> UserProfile
          ├─> QuizAttempt
          └─> Certificate
```

## 🚀 Testing Phase 2

1. **Enroll in a course**
2. **Complete lessons** - Mark as complete
3. **Take quizzes** - Test assessments
4. **Complete course** - Get certificate
5. **View profile** - See statistics
6. **Search courses** - Use filters
7. **Instructor view** - Check dashboard

## 📝 Notes

- All views are login-protected
- Progress is tracked automatically
- Certificates auto-generate on course completion
- Quizzes support multiple choice and true/false
- Profile avatars use URLs (Gravatar, etc.)
- Search is case-insensitive
- Categories are optional for courses

---

**Phase 2 adds professional-grade learning management features to your platform!** 🎓
