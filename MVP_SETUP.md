# MVP Setup Guide - Ctrl+Shift Academy

This guide will help you set up the MVP (Minimum Viable Product) version of Ctrl+Shift Academy with full course and lesson functionality.

## What's Included in MVP

✅ **Complete Authentication System**
- User registration with email verification
- Login/logout functionality
- Password security

✅ **Course Management**
- Course listing dashboard
- Course detail pages
- Lesson viewer with navigation
- Django admin interface for content management

✅ **Data Models**
- Course model (title, description, instructor, slug)
- Lesson model (title, content, order, slug)
- Relationships and ordering

✅ **Sample Content**
- 3 pre-built courses with lessons
- Python Programming course
- Web Development course
- Database Design course

## Quick Start (Automated)

Run the automated setup script:

```bash
cd /var/www/html/contract/mwangi_jeremiah/classes
./setup_mvp.sh
```

The script will:
1. Check/create virtual environment
2. Install dependencies
3. Create and run migrations
4. Optionally create superuser
5. Optionally seed sample data

## Manual Setup

If you prefer manual setup:

### 1. Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python3 manage.py createsuperuser
```

### 5. Seed Sample Data (Optional)

```bash
python3 manage.py seed_data
```

This creates:
- 3 sample courses with lessons
- An instructor account (username: `instructor`, password: `instructor123`)

### 6. Run Development Server

```bash
python3 manage.py runserver
```

## Access Points

- **Main Dashboard**: http://127.0.0.1:8000/
- **Registration**: http://127.0.0.1:8000/authentication/register/
- **Login**: http://127.0.0.1:8000/authentication/login/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## MVP Features Overview

### For Students (Logged-in Users)

1. **Dashboard** (`/`)
   - View all available courses
   - See course descriptions and lesson counts
   - Quick access to courses

2. **Course Detail** (`/course/{slug}/`)
   - Full course information
   - Complete lesson list
   - One-click access to lessons

3. **Lesson Viewer** (`/course/{slug}/lesson/{slug}/`)
   - Full lesson content
   - Previous/Next navigation
   - Course outline sidebar
   - Progress tracking (visual)

### For Instructors/Admins

1. **Django Admin Panel** (`/admin/`)
   - Create/edit courses
   - Add/manage lessons
   - Reorder lessons
   - Publish/unpublish courses
   - User management

## Creating Your First Course

### Via Django Admin

1. Navigate to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Click "Courses" → "Add Course"
4. Fill in:
   - Title
   - Description
   - Select instructor
   - Check "Is published"
5. Save the course
6. Click "Lessons" → "Add Lesson"
7. Fill in:
   - Select course
   - Title
   - Content (supports line breaks)
   - Order (0, 1, 2, etc.)
8. Save the lesson
9. Repeat for more lessons

### Course Fields Explained

**Course Model:**
- `title`: Course name (e.g., "Python Programming")
- `slug`: Auto-generated URL-friendly version
- `description`: Full course description
- `instructor`: Select from registered users
- `is_published`: Show/hide course from students
- `created_at`: Auto-generated timestamp

**Lesson Model:**
- `course`: Parent course
- `title`: Lesson name (e.g., "Variables and Data Types")
- `slug`: Auto-generated URL-friendly version
- `content`: Full lesson text (HTML safe, use line breaks)
- `order`: Display order (0=first, 1=second, etc.)
- `created_at`: Auto-generated timestamp

## User Flow

### New User Registration

1. Visit `/authentication/register/`
2. Fill in username, email, password
3. Real-time validation checks availability
4. Submit form
5. Check email/console for activation link
6. Click activation link
7. Account activated → Login

### Existing User Login

1. Visit `/authentication/login/`
2. Enter username and password
3. Redirected to dashboard
4. View and access courses

### Taking a Course

1. From dashboard, click "View Course"
2. See course overview and lesson list
3. Click any lesson to start
4. Read lesson content
5. Use "Previous" / "Next" buttons to navigate
6. Click "Course Complete" on final lesson

## Customization Tips

### Change Course Layout

Edit: `templates/lessons/index.html`
- Modify card design
- Change grid columns (col-md-4, col-md-6, etc.)
- Add filters or search

### Customize Lesson Viewer

Edit: `templates/lessons/lesson_detail.html`
- Adjust content styling
- Add progress bar
- Include quizzes or exercises

### Update Navigation

Edit: `templates/partials/_sidebar.html`
- Add new menu items
- Change icons (Feather Icons)
- Add external links

### Styling

Files to modify:
- `classes/static/css/main.css` - Global styles
- `classes/static/css/dashboard.css` - Dashboard specific
- Use Bootstrap classes in templates

## Troubleshooting

### Migrations Error

```bash
# Reset migrations (⚠️ destroys data)
python3 manage.py migrate lessons zero
python3 manage.py migrate

# Or drop and recreate database
```

### No Courses Showing

Check:
1. Courses exist: `python3 manage.py shell` → `from lessons.models import Course; Course.objects.all()`
2. Courses are published: Check `is_published=True` in admin
3. User is logged in

### Lessons Not Ordered

In Django admin:
1. Go to Lessons
2. Set `order` field (0, 1, 2, 3...)
3. Save changes

### Static Files Not Loading

```bash
python3 manage.py collectstatic
```

## Next Steps for Production

- [ ] Add user progress tracking
- [ ] Implement course enrollment
- [ ] Add completion certificates
- [ ] Create quiz/assessment system
- [ ] Add user profiles
- [ ] Implement course search
- [ ] Add course categories
- [ ] Create instructor dashboard
- [ ] Add file attachments to lessons
- [ ] Implement discussion forums

## Database Schema

### Course Table
```sql
- id (Primary Key)
- title (VARCHAR)
- slug (SLUG, Unique)
- description (TEXT)
- instructor_id (Foreign Key → User)
- is_published (BOOLEAN)
- created_at (DATETIME)
- updated_at (DATETIME)
```

### Lesson Table
```sql
- id (Primary Key)
- course_id (Foreign Key → Course)
- title (VARCHAR)
- slug (SLUG)
- content (TEXT)
- order (INTEGER)
- created_at (DATETIME)
- updated_at (DATETIME)
```

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review Django error messages
3. Check database configuration in .env
4. Verify PostgreSQL is running

---

**Happy Teaching & Learning! 🎓**
