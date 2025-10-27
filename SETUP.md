# Classes Application - Setup Guide

A Django-based learning management system with real-time chat functionality using WebSockets.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Application Features](#application-features)
- [Troubleshooting](#troubleshooting)

---

## Features

### 1. **Authentication System**
- User registration with email verification
- Login/Logout functionality
- Username and email validation
- Password reset capability

### 2. **Learning Management (Lessons)**
- Course catalog and browsing
- Course enrollment
- Lesson content (video and text)
- Progress tracking
- Quiz functionality
- Certificates upon course completion
- Instructor dashboard
- User profiles

### 3. **Real-time Chat**
- WebSocket-based chat rooms
- Multiple channels support
- Real-time message broadcasting
- Message history persistence
- User identification in messages

---

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.10+**
- **PostgreSQL** (running and accessible)
- **Redis Server** (for WebSocket channel layer)
- **pip** (Python package manager)
- **virtualenv** or **venv**

### Check Prerequisites

```bash
# Check Python version
python3 --version

# Check PostgreSQL
psql --version

# Check Redis
redis-cli ping  # Should return PONG
```

---

## Installation

### 1. Clone or Navigate to Project Directory

```bash
cd /var/www/html/contract/mwangi_jeremiah/classes
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

The `.env` file has been created with the following configuration:

```env
# Database Configuration
DB_NAME=classes_db
DB_USER=kimemia
DB_PASSWORD=@K1m3m14
DB_HOST=localhost

# Redis Configuration
REDIS_HOST=localhost

# Email Configuration (optional - currently using console backend)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password
```

**Note:** Email is currently configured to use Django's console backend for development (emails will print to console).

---

## Database Setup

### Automated Setup (Recommended)

Run the database setup script:

```bash
./setup_database.sh
```

This script will:
- Create the PostgreSQL database `classes_db`
- Run all Django migrations
- Prompt you to create a superuser (optional)

### Manual Setup

If you prefer manual setup:

```bash
# 1. Create database
export PGPASSWORD='@K1m3m14'
createdb -h localhost -U kimemia classes_db

# 2. Run migrations
.venv/bin/python manage.py makemigrations
.venv/bin/python manage.py migrate

# 3. Create superuser (optional)
.venv/bin/python manage.py createsuperuser
```

---

## Running the Application

### Quick Start

```bash
./start_server.sh
```

The server will start on `http://localhost:8000`

### Manual Start

If you prefer to start manually:

```bash
# Activate virtual environment
source .venv/bin/activate

# Start Daphne ASGI server (supports WebSockets)
daphne -b 0.0.0.0 -p 8000 classes.asgi:application
```

**Important:** Use **Daphne** (not Django's runserver) to enable WebSocket functionality for the chat feature.

### Alternative: Django Development Server (Limited)

For development without chat features:

```bash
python manage.py runserver
```

**Note:** Django's runserver does NOT support WebSockets, so the chat feature will not work properly.

---

## Application Features

### Accessing the Application

Once the server is running, access these URLs:

| Feature | URL |
|---------|-----|
| **Home/Lessons** | http://localhost:8000/ |
| **User Registration** | http://localhost:8000/authentication/register/ |
| **User Login** | http://localhost:8000/authentication/login/ |
| **Chat Rooms** | http://localhost:8000/chat/ |
| **Admin Panel** | http://localhost:8000/admin/ |
| **User Profile** | http://localhost:8000/profile/ |
| **My Courses** | http://localhost:8000/my-courses/ |
| **Instructor Dashboard** | http://localhost:8000/instructor/dashboard/ |

### 1. Authentication

**Registration Flow:**
1. Navigate to `/authentication/register/`
2. Fill in username, email, and password
3. Account activation (currently console-based email)
4. Login at `/authentication/login/`

**Features:**
- Real-time username validation
- Real-time email validation
- Email verification tokens
- Secure password handling

### 2. Learning Management System

**For Students:**
- Browse available courses
- Enroll in courses
- Access lesson content (videos/text)
- Complete lessons and track progress
- Take quizzes
- Earn certificates upon course completion
- View profile and enrolled courses

**For Instructors:**
- Access instructor dashboard
- Manage courses
- Track student progress

### 3. Real-time Chat

**Features:**
- Create chat channels/rooms
- Real-time message delivery via WebSockets
- Message history persistence
- User identification
- Multiple concurrent rooms

**How to Use:**
1. Navigate to `/chat/`
2. Create a new channel or select existing one
3. Type messages and press Send or Enter
4. Messages appear in real-time for all connected users

**Technical Details:**
- WebSocket endpoint: `ws://localhost:8000/ws/chat/<room_name>/`
- Uses Django Channels with Redis backend
- Automatic reconnection on disconnect

---

## Project Structure

```
classes/
├── authentication/          # User authentication app
│   ├── views.py            # Registration, login, validation
│   ├── models.py           # Custom user models (if any)
│   └── urls.py             # Auth URL patterns
├── lessons/                # Learning management app
│   ├── models.py           # Course, Lesson, Quiz models
│   ├── views.py            # Course and lesson views
│   └── urls.py             # Lesson URL patterns
├── chat/                   # Real-time chat app
│   ├── consumer.py         # WebSocket consumer
│   ├── routing.py          # WebSocket URL routing
│   ├── models.py           # Channel and Message models
│   ├── views.py            # HTTP views for chat
│   └── urls.py             # HTTP URL patterns
├── classes/                # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── asgi.py             # ASGI config for WebSockets
│   └── wsgi.py             # WSGI config
├── templates/              # HTML templates
│   ├── authentication/
│   ├── lessons/
│   ├── chat/
│   └── base.html
├── static/                 # Static files (CSS, JS)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── start_server.sh        # Server startup script
├── setup_database.sh      # Database setup script
└── SETUP.md              # This file
```

---

## Troubleshooting

### Issue: Database Connection Errors

```
django.db.utils.OperationalError: could not connect to server
```

**Solution:**
1. Check PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify credentials in `.env` file
3. Test connection: `psql -h localhost -U kimemia -d classes_db`

### Issue: Chat Messages Not Appearing

**Symptoms:** Messages don't display in real-time

**Possible Causes & Solutions:**

1. **Redis not running:**
   ```bash
   sudo systemctl start redis
   redis-cli ping  # Should return PONG
   ```

2. **Using Django runserver instead of Daphne:**
   - Stop the server
   - Start with: `./start_server.sh` or `daphne classes.asgi:application`

3. **WebSocket connection failed:**
   - Check browser console for WebSocket errors
   - Verify URL pattern in `chat/routing.py` matches JavaScript
   - Ensure `channels` is in `INSTALLED_APPS`

### Issue: Static Files Not Loading

```
GET /static/... 404 (Not Found)
```

**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: Migration Errors

```
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Solution:**
```bash
# Reset migrations (CAUTION: Development only!)
python manage.py migrate --fake-initial
```

### Issue: Import Errors (environ module)

```
ModuleNotFoundError: No module named 'environ'
```

**Solution:**
```bash
# Uninstall old environ package
pip uninstall -y environ
# Install correct package
pip install django-environ
```

### Issue: Permission Denied on Scripts

```
bash: ./start_server.sh: Permission denied
```

**Solution:**
```bash
chmod +x start_server.sh setup_database.sh
```

---

## Development Notes

### Creating a Superuser

To access the admin panel:

```bash
python manage.py createsuperuser
```

Follow prompts to set username, email, and password.

### Running Tests

```bash
python manage.py test
```

### Checking for Issues

```bash
# Basic check
python manage.py check

# Deployment check (shows security warnings)
python manage.py check --deploy
```

### Database Migrations

When you modify models:

```bash
# Generate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations
```

---

## Key Technologies

- **Django 5.2.7** - Web framework
- **Django Channels** - WebSocket support
- **PostgreSQL** - Database
- **Redis** - Channel layer backend
- **Daphne** - ASGI server
- **Bootstrap** - Frontend framework

---

## Security Notes for Production

The current setup is configured for **LOCAL DEVELOPMENT ONLY**. Before deploying to production:

1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use proper SSL/TLS certificates
5. Set secure cookie flags
6. Use environment variables for all secrets
7. Configure proper email backend (not console)
8. Set up proper logging
9. Use production-grade ASGI server (Daphne with supervisor/systemd)
10. Configure firewall rules

---

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review Django logs in the console
3. Check browser console for JavaScript errors (F12)
4. Verify all services are running (PostgreSQL, Redis)

---

## Quick Reference Commands

```bash
# Start server
./start_server.sh

# Stop server
Ctrl+C

# Check database
psql -h localhost -U kimemia -d classes_db

# Check Redis
redis-cli ping

# Activate virtual environment
source .venv/bin/activate

# View logs (server must be running)
# Logs appear in the terminal where server is running

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

---

**Last Updated:** October 27, 2025
**Application Version:** 1.0.0
**Django Version:** 5.2.7
