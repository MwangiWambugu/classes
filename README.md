# Ctrl+Shift Academy Platform

A Django-based learning management system featuring user authentication, email verification, and a lesson dashboard. This platform is designed to provide a gated learning experience where users must register and verify their accounts before accessing course content.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Application Flow](#application-flow)
- [Core Components](#core-components)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Known Issues](#known-issues)
- [Future Enhancements](#future-enhancements)

---

## Overview

**Ctrl+Shift Academy** is a Django 5.2.7 web application built to prototype an online learning platform with the following key features:

- **User Registration & Authentication**: Complete signup flow with email validation
- **Email Verification**: Account activation via secure email tokens
- **Login-Protected Dashboard**: Lesson content accessible only to authenticated users
- **Real-time Form Validation**: AJAX-powered username and email validation during registration
- **Responsive UI**: Bootstrap 4-based interface with custom styling

The application currently focuses on authentication infrastructure and dashboard scaffolding. Lesson content models and business logic are planned for future iterations.

---

## Architecture

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend Framework** | Django | 5.2.7 |
| **Database** | PostgreSQL | Latest |
| **Frontend Framework** | Bootstrap | 4.x |
| **JavaScript Library** | jQuery | 3.4.1 |
| **Python Environment** | Python | 3.12+ |
| **Email Backend** | Console (Dev) | - |

### Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Django Application                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐         ┌─────────────────┐           │
│  │  Authentication │         │    Lessons      │           │
│  │      App        │         │      App        │           │
│  │                 │         │                 │           │
│  │ • Registration  │         │ • Dashboard     │           │
│  │ • Login/Logout  │────────▶│ • (Future:      │           │
│  │ • Verification  │         │   Course Models)│           │
│  │ • AJAX Validation│        │                 │           │
│  └─────────────────┘         └─────────────────┘           │
│         │                            │                       │
│         └────────────┬───────────────┘                       │
│                      │                                        │
│         ┌────────────▼──────────────┐                       │
│         │   Django ORM / Models     │                       │
│         │   (Using built-in User)   │                       │
│         └────────────┬──────────────┘                       │
│                      │                                        │
│         ┌────────────▼──────────────┐                       │
│         │   PostgreSQL Database     │                       │
│         └───────────────────────────┘                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Design Patterns

- **Class-Based Views (CBVs)**: All views use Django's View class for better code organization
- **Template Inheritance**: Base templates (`base.html`, `base_auth.html`) provide consistent layouts
- **Component-Based UI**: Reusable partials (`_messages.html`, `_sidebar.html`) for modular design
- **Token-Based Verification**: Custom token generator extending Django's `PasswordResetTokenGenerator`
- **Environment-Based Configuration**: Sensitive data managed via `.env` file

---

## Project Structure

```
/var/www/html/contract/mwangi_jeremiah/classes/
│
├── authentication/              # Authentication app
│   ├── migrations/              # Database migrations (none yet)
│   ├── __pycache__/            # Python bytecode cache
│   ├── admin.py                # Admin configuration (empty)
│   ├── apps.py                 # App configuration
│   ├── models.py               # Models (uses Django's User model)
│   ├── tests.py                # Unit tests (not implemented)
│   ├── urls.py                 # URL routing for auth endpoints
│   ├── utils.py                # Custom token generator
│   └── views.py                # Authentication views (CBVs)
│
├── lessons/                     # Lessons app
│   ├── migrations/              # Database migrations
│   ├── __pycache__/            # Python bytecode cache
│   ├── admin.py                # Admin configuration (empty)
│   ├── apps.py                 # App configuration
│   ├── models.py               # Models (none defined yet)
│   ├── tests.py                # Unit tests (not implemented)
│   ├── urls.py                 # URL routing for lessons
│   └── views.py                # Lessons dashboard view
│
├── classes/                     # Django project configuration
│   ├── static/                  # Static assets
│   │   ├── css/                # Stylesheets
│   │   │   ├── bootstrap.min.css
│   │   │   ├── dashboard.css
│   │   │   └── main.css
│   │   └── js/                 # JavaScript files
│   │       ├── main.js         # Main JS (minimal)
│   │       └── register.js     # Registration AJAX validation
│   ├── __pycache__/            # Python bytecode cache
│   ├── __init__.py             # Python package marker
│   ├── asgi.py                 # ASGI configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI configuration
│
├── templates/                   # HTML templates
│   ├── authentication/          # Auth-related templates
│   │   ├── login.html          # Login form
│   │   ├── register.html       # Registration form
│   │   ├── reset-password.html # Password reset (not wired)
│   │   └── set-newpassword.html # Set new password (not wired)
│   ├── lessons/                 # Lessons templates
│   │   └── index.html          # Dashboard (empty content)
│   ├── partials/                # Reusable components
│   │   ├── _messages.html      # Django messages display
│   │   └── _sidebar.html       # Dashboard sidebar navigation
│   ├── base.html               # Authenticated layout
│   ├── base_auth.html          # Public pages layout
│   └── index.html              # (Not used currently)
│
├── .venv/                       # Virtual environment
├── py312/                       # Alternative virtual environment
├── .git/                        # Git repository
├── .idea/                       # IDE configuration
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── manage.py                    # Django management script
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

---

## Application Flow

### 1. User Registration Flow

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       │ GET /authentication/register/
       ▼
┌──────────────────────────────────────┐
│  registrationView.get()              │
│  • Renders registration form         │
└──────────────┬───────────────────────┘
               │
               │ User fills form
               │ • JavaScript validates username/email via AJAX
               │ • POST /authentication/validate_username/
               │ • POST /authentication/validate_email/
               ▼
┌──────────────────────────────────────┐
│  UsernameValidationView.post()       │
│  emailValidationView.post()          │
│  • Check if username/email exists    │
│  • Validate format                   │
│  • Return JSON response              │
└──────────────┬───────────────────────┘
               │
               │ User submits form
               ▼
┌──────────────────────────────────────┐
│  registrationView.post()             │
│  1. Validate username (unique)       │
│  2. Validate email (unique)          │
│  3. Validate password (min 6 chars)  │
│  4. Create User (is_active=False)    │
│  5. Generate activation token        │
│  6. Build activation URL             │
│  7. Send activation email            │
│  8. Display success message          │
└──────────────┬───────────────────────┘
               │
               │ Email sent to user
               ▼
┌──────────────────────────────────────┐
│  Email Inbox                         │
│  Subject: "Activate your account"    │
│  Body: Activation link with token    │
└──────────────┬───────────────────────┘
               │
               │ User clicks link
               │ GET /authentication/activate/<uidb64>/<token>/
               ▼
┌──────────────────────────────────────┐
│  verificationView.get()              │
│  1. Decode user ID from uidb64       │
│  2. Fetch User object                │
│  3. Validate token                   │
│  4. Check if already active          │
│  5. Set user.is_active = True        │
│  6. Save user                        │
│  7. Redirect to login                │
└──────────────┬───────────────────────┘
               │
               ▼
       Registration Complete
```

### 2. Login Flow

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       │ GET /authentication/login/
       ▼
┌──────────────────────────────────────┐
│  loginView.get()                     │
│  • Renders login form                │
└──────────────┬───────────────────────┘
               │
               │ User submits credentials
               │ POST /authentication/login/
               ▼
┌──────────────────────────────────────┐
│  loginView.post()                    │
│  1. Get username & password          │
│  2. Authenticate user                │
│  3. Check if user is active          │
│  4. Create session (login)           │
│  5. Redirect to lessons dashboard    │
└──────────────┬───────────────────────┘
               │
               │ Success
               ▼
┌──────────────────────────────────────┐
│  lessons.views.home()                │
│  • @login_required decorator         │
│  • Renders lessons/index.html        │
└──────────────────────────────────────┘
```

### 3. Lessons Dashboard Access Flow

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       │ GET /
       ▼
┌──────────────────────────────────────┐
│  lessons.views.home()                │
│  @login_required(                    │
│      login_url='/authentication/login/')│
└──────────────┬───────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        │ Authenticated?
        │             │
    ┌───▼──┐      ┌───▼──┐
    │ Yes  │      │  No  │
    └───┬──┘      └───┬──┘
        │             │
        │             │ Redirect to login
        │             ▼
        │      /authentication/login/
        │
        │ Render lessons/index.html
        ▼
    Dashboard
```

### 4. Logout Flow

```
┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       │ POST /authentication/logout/
       ▼
┌──────────────────────────────────────┐
│  logoutView.post()                   │
│  1. Call auth.logout(request)        │
│  2. Destroy session                  │
│  3. Display success message          │
│  4. Redirect to login                │
└──────────────────────────────────────┘
```

---

## Core Components

### 1. Authentication App (`authentication/`)

#### **Views** (`views.py`)

All views are class-based views (CBVs) inheriting from `django.views.View`:

**a) `UsernameValidationView`**
- **Purpose**: AJAX endpoint for real-time username validation
- **Method**: POST
- **Validation**:
  - Alphanumeric characters only
  - Username must be unique
- **Response**: JSON with `username_error` or `username_valid`

**b) `emailValidationView`**
- **Purpose**: AJAX endpoint for real-time email validation
- **Method**: POST
- **Validation**:
  - Valid email format (via `validate_email` library)
  - Email must be unique
- **Response**: JSON with `email_error` or `email_valid`

**c) `registrationView`**
- **GET**: Renders registration form
- **POST**:
  - Validates username, email, password
  - Creates inactive user (`is_active=False`)
  - Generates activation token via `token_generator`
  - Builds activation URL with encoded user ID and token
  - Sends activation email
  - Displays success message
- **Business Rules**:
  - Username must be unique
  - Email must be unique
  - Password minimum length: 6 characters

**d) `verificationView`**
- **Purpose**: Activates user account via email link
- **Method**: GET
- **Process**:
  1. Decode `uidb64` to get user ID
  2. Fetch user from database
  3. Validate token using `token_generator`
  4. Check if user is already active
  5. Set `user.is_active = True`
  6. Save user and redirect to login
- **Error Handling**: Redirects to login on any exception

**e) `loginView`**
- **GET**: Renders login form
- **POST**:
  - Validates credentials
  - Checks if account is active
  - Creates session via `auth.login()`
  - Redirects to lessons dashboard
- **Error Messages**:
  - "Account is not active, please check your email"
  - "Invalid credentials, please try again"

**f) `logoutView`**
- **POST**: Logs out user and redirects to login
- **GET**: Redirects to login (no logout action)

#### **Utilities** (`utils.py`)

**`appTokenGenerator`**
- Extends `PasswordResetTokenGenerator`
- Custom hash includes:
  - User primary key
  - Timestamp
  - User's `is_active` status
- **Purpose**: Token becomes invalid once account is activated, preventing reuse of activation links

#### **URL Patterns** (`urls.py`)

| URL Pattern | View | Name | CSRF |
|------------|------|------|------|
| `/authentication/register/` | `registrationView` | `register` | Protected |
| `/authentication/validate_username/` | `UsernameValidationView` | `validate_username` | **Exempt** |
| `/authentication/validate_email/` | `emailValidationView` | `validate_email` | **Exempt** |
| `/authentication/activate/<uidb64>/<token>/` | `verificationView` | `activate` | Protected |
| `/authentication/login/` | `loginView` | `login` | Protected |
| `/authentication/logout/` | `logoutView` | `logout` | Protected |

**Note**: AJAX validation endpoints are CSRF-exempt for easier frontend integration.

---

### 2. Lessons App (`lessons/`)

#### **Views** (`views.py`)

**`home(request)`**
- **Decorator**: `@login_required(login_url='/authentication/login/')`
- **Purpose**: Renders the lessons dashboard
- **Current State**: Template is empty (no lesson content)
- **Future**: Will display courses, lessons, and user progress

#### **URL Patterns** (`urls.py`)

| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `/` | `home` | `lessons` | Main dashboard |

---

### 3. Templates

#### **Base Templates**

**a) `base.html`** (Authenticated Users)
- **Components**:
  - Top navigation bar with branding
  - User display (username)
  - Logout form (POST with CSRF token)
  - Left sidebar navigation
  - Main content area
- **JavaScript Libraries**:
  - jQuery 3.4.1
  - Feather Icons 4.9.0
  - Chart.js 2.7.3
- **Static Assets**:
  - Bootstrap CSS
  - Custom CSS (main.css, dashboard.css)
  - Custom JS (main.js)

**b) `base_auth.html`** (Public Pages)
- **Purpose**: Minimal layout for login/registration
- **Components**:
  - Basic HTML structure
  - Same CSS/JS as base.html
  - No navigation or sidebar
  - Clean content area

#### **Authentication Templates**

**a) `register.html`**
- Extends `base_auth.html`
- **Form Fields**:
  - Username (with real-time validation)
  - Email (with real-time validation)
  - Password (with show/hide toggle)
- **Features**:
  - AJAX validation feedback areas
  - Link to login page
  - Django messages integration
- **JavaScript**: Includes `register.js`

**b) `login.html`**
- Extends `base_auth.html`
- **Form Fields**:
  - Username
  - Password
- **Features**:
  - Django messages integration
  - Simple form submission

#### **Partials**

**a) `_messages.html`**
- Displays Django flash messages
- Uses Bootstrap alert styling
- Supports message tags (success, error, warning, info)

**b) `_sidebar.html`**
- Left sidebar navigation
- **Navigation Items**:
  - Dashboard
  - Explore Courses (no href)
  - Class Sessions (no href)
  - Submissions (no href)
  - Groups (no href)
  - Community (no href)
- **Settings Section**:
  - General (no href)
  - Account (no href)
- **Note**: Most links are placeholders

#### **Lessons Templates**

**a) `lessons/index.html`**
- Extends `base.html`
- **Current State**: Empty content block (commented out welcome message)
- **Future**: Will display lessons, progress, and course materials

---

### 4. Static Assets

#### **CSS Files**

- **`bootstrap.min.css`**: Bootstrap 4 framework
- **`main.css`**: Custom application styles
- **`dashboard.css`**: Dashboard-specific styles

#### **JavaScript Files**

**a) `register.js`** (Primary Registration Logic)

**Features**:

1. **Password Visibility Toggle**
   - Toggles between `password` and `text` input types
   - Button text switches between "SHOW" and "HIDE"

2. **Email Validation** (Keyup Event)
   - Sends POST request to `/authentication/validate_email/`
   - Real-time feedback on email validity
   - Disables submit button on error
   - Updates UI with error messages

3. **Username Validation** (Keyup Event)
   - Sends POST request to `/authentication/validate_username/`
   - Real-time feedback on username validity
   - Disables submit button on error
   - Updates UI with error messages

**Code Structure**:
```javascript
// Element selections
const usernamefield = document.querySelector('#usernameField');
const emailField = document.querySelector('#emailField');
const passwordField = document.querySelector('#passwordField');
const submitBtn = document.querySelector('.submit_btn');

// Event listeners
showPasswordToggle.addEventListener('click', handleToggleInput);
emailField.addEventListener("keyup", validateEmail);
usernamefield.addEventListener("keyup", validateUsername);
```

**b) `main.js`**
- Currently minimal: `console.log("Hello, world!");`
- Placeholder for future dashboard functionality

---

### 5. Configuration (`classes/settings.py`)

#### **Core Settings**

```python
# Security
SECRET_KEY = "django-insecure-tf0-@e#c!i@qi@^$0f2u3ve#ry9o4cniecv=00g8e^e932bj-d"
DEBUG = True  # ⚠️ Set to False in production
ALLOWED_HOSTS = []  # ⚠️ Configure for production

# Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "lessons",  # Custom app
]
# ⚠️ Note: 'authentication' app is NOT registered in INSTALLED_APPS

# Database (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
    }
}

# Static Files
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "classes/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Email Configuration (Development)
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_USE_TLS = True  # ⚠️ Typo in original: EMAIL_USER_TLS
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### **Important Notes**

1. **Missing Authentication App**: The `authentication` app is not listed in `INSTALLED_APPS`, but it still works because it doesn't define models or migrations
2. **Typo in Settings**: `EMAIL_USER_TLS` should be `EMAIL_USE_TLS` (line 142)
3. **Console Email Backend**: Emails print to console instead of sending via SMTP

---

## Setup & Installation

### Prerequisites

- Python 3.12+
- PostgreSQL (any recent version)
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd classes
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies** (`requirements.txt`):
```
django==5.2.7
psycopg2-binary
environ
validate-email
six
```

### Step 4: Configure Database

**Create PostgreSQL Database:**

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE usersdb;
CREATE USER postgres WITH PASSWORD 'password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE usersdb TO postgres;
\q
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
DB_NAME=usersdb
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost

# Email Configuration (Optional for development)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**Note**: The console email backend is active by default, so email configuration is optional for development.

### Step 6: Run Migrations

```bash
python manage.py migrate
```

This will create all necessary database tables, including:
- Django's built-in tables (auth_user, sessions, admin, etc.)
- No custom app tables (authentication and lessons have no models)

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 8: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

### Step 9: Access the Application

- **Lessons Dashboard**: http://127.0.0.1:8000/ (requires login)
- **Register**: http://127.0.0.1:8000/authentication/register/
- **Login**: http://127.0.0.1:8000/authentication/login/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Configuration

### Environment Variables (`.env`)

| Variable | Purpose | Example | Required |
|----------|---------|---------|----------|
| `DB_NAME` | PostgreSQL database name | `usersdb` | Yes |
| `DB_USER` | PostgreSQL username | `postgres` | Yes |
| `DB_PASSWORD` | PostgreSQL password | `password` | Yes |
| `DB_HOST` | PostgreSQL host | `localhost` | Yes |
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` | No (dev) |
| `EMAIL_HOST_USER` | SMTP username | `email@example.com` | No (dev) |
| `EMAIL_HOST_PASSWORD` | SMTP password | `app-password` | No (dev) |
| `DEFAULT_FROM_EMAIL` | Default sender email | `noreply@example.com` | No (dev) |

### Email Backend Configuration

**Development (Current)**:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Activation emails print to console/terminal.

**Production (Recommended)**:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
Activation emails sent via SMTP server.

### Static Files

**Development**:
```bash
# Static files served automatically by runserver
# No action needed
```

**Production**:
```bash
# Collect static files
python manage.py collectstatic
```

This copies all static files from `classes/static/` to `STATIC_ROOT` (`/static/`).

---

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Authentication | Response |
|--------|----------|-------------|----------------|----------|
| GET | `/` | Lessons dashboard | Required | HTML |
| GET | `/authentication/register/` | Registration form | Public | HTML |
| POST | `/authentication/register/` | Create new account | Public | Redirect/HTML |
| GET | `/authentication/login/` | Login form | Public | HTML |
| POST | `/authentication/login/` | Authenticate user | Public | Redirect/HTML |
| POST | `/authentication/logout/` | Logout user | Required | Redirect |
| GET | `/authentication/activate/<uidb64>/<token>/` | Activate account | Public | Redirect |
| POST | `/authentication/validate_username/` | Validate username (AJAX) | Public | JSON |
| POST | `/authentication/validate_email/` | Validate email (AJAX) | Public | JSON |
| GET | `/admin/` | Django admin panel | Admin only | HTML |

### AJAX Validation Endpoints

#### Validate Username

**Endpoint**: `POST /authentication/validate_username/`

**Request Body**:
```json
{
  "username": "john_doe"
}
```

**Success Response** (200):
```json
{
  "username_valid": true
}
```

**Error Response** (400):
```json
{
  "username_error": "username should only contain alphanumeric characters"
}
```
or
```json
{
  "username_error": "Sorry Username in Use"
}
```

#### Validate Email

**Endpoint**: `POST /authentication/validate_email/`

**Request Body**:
```json
{
  "email": "john@example.com"
}
```

**Success Response** (200):
```json
{
  "email_valid": true
}
```

**Error Response** (400):
```json
{
  "email_error": "email is invalid"
}
```
or
```json
{
  "email_error": "Sorry email in Use"
}
```

---

## Known Issues

### Critical Issues

1. **Authentication App Not Registered**
   - **Issue**: `authentication` is not in `INSTALLED_APPS` in `settings.py`
   - **Impact**: App works because no models are defined, but may cause issues with Django tools
   - **Fix**: Add `"authentication"` to `INSTALLED_APPS` list

2. **Email Configuration Typo**
   - **Issue**: `EMAIL_USER_TLS` instead of `EMAIL_USE_TLS` in `settings.py:142`
   - **Impact**: TLS may not be properly configured
   - **Fix**: Change `EMAIL_USER_TLS` to `EMAIL_USE_TLS`

### Minor Issues

3. **Empty Lessons Dashboard**
   - **Issue**: `lessons/index.html` has no content
   - **Impact**: Users see blank page after login
   - **Recommendation**: Add welcome message or dashboard widgets

4. **Sidebar Links Missing Hrefs**
   - **Issue**: Most sidebar links have empty `href=""` attributes
   - **Impact**: Links do nothing when clicked
   - **Recommendation**: Add proper URLs or remove inactive links

5. **No Lesson Models**
   - **Issue**: No data models defined for courses, lessons, or progress
   - **Impact**: Cannot store or display learning content
   - **Recommendation**: Design and implement lesson data schema

6. **No Automated Tests**
   - **Issue**: `tests.py` files are empty in both apps
   - **Impact**: No test coverage for authentication or lesson logic
   - **Recommendation**: Implement unit and integration tests

7. **Password Reset Not Implemented**
   - **Issue**: Templates exist (`reset-password.html`, `set-newpassword.html`) but not wired up
   - **Impact**: Users cannot reset forgotten passwords
   - **Recommendation**: Implement password reset flow

8. **No Admin Interface Configuration**
   - **Issue**: `admin.py` files are empty
   - **Impact**: Cannot manage users or future models via Django admin
   - **Recommendation**: Register User model in authentication/admin.py

### Security Concerns

9. **Debug Mode Enabled**
   - **Issue**: `DEBUG = True` in `settings.py`
   - **Risk**: Exposes sensitive error information
   - **Fix**: Set `DEBUG = False` in production

10. **Secret Key Exposed**
    - **Issue**: `SECRET_KEY` hardcoded in `settings.py`
    - **Risk**: Security vulnerability if code is public
    - **Fix**: Move `SECRET_KEY` to `.env` file

11. **Empty ALLOWED_HOSTS**
    - **Issue**: `ALLOWED_HOSTS = []` in `settings.py`
    - **Risk**: Won't work in production
    - **Fix**: Add production domain(s) to `ALLOWED_HOSTS`

---

## Future Enhancements

### Phase 1: Core Functionality

- [ ] Add `authentication` to `INSTALLED_APPS`
- [ ] Fix `EMAIL_USE_TLS` typo
- [ ] Add content to lessons dashboard
- [ ] Implement lesson data models (Course, Lesson, Progress)
- [ ] Add password reset functionality
- [ ] Configure Django admin interface

### Phase 2: User Experience

- [ ] Implement course catalog page
- [ ] Add user profile page
- [ ] Create progress tracking system
- [ ] Add lesson content viewer
- [ ] Implement quiz/assessment system
- [ ] Add notification system

### Phase 3: Testing & Quality

- [ ] Write unit tests for authentication
- [ ] Write integration tests for registration flow
- [ ] Add test coverage for lesson views
- [ ] Implement CI/CD pipeline
- [ ] Add code quality checks (linting, formatting)

### Phase 4: Production Readiness

- [ ] Move `SECRET_KEY` to environment variables
- [ ] Configure SMTP email backend
- [ ] Set up production database
- [ ] Configure static file serving (CDN/S3)
- [ ] Add logging and monitoring
- [ ] Implement rate limiting
- [ ] Add HTTPS support
- [ ] Configure `ALLOWED_HOSTS` for production

### Phase 5: Advanced Features

- [ ] Add multi-language support (i18n)
- [ ] Implement role-based access control (instructor/student)
- [ ] Add file upload for assignments
- [ ] Create instructor dashboard
- [ ] Add discussion forums
- [ ] Implement real-time notifications
- [ ] Add video streaming support
- [ ] Create mobile-responsive design improvements

---

## Database Schema

Currently, the application uses Django's built-in `User` model from `django.contrib.auth`. No custom models are defined.

### Current Tables (Django Default)

- **auth_user**: User accounts
- **auth_group**: Permission groups
- **auth_permission**: Permissions
- **django_session**: Session data
- **django_admin_log**: Admin action logs
- **django_content_type**: Content type registry
- **django_migrations**: Migration history

### Proposed Schema (Future)

```sql
-- Courses
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    instructor_id INTEGER REFERENCES auth_user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Lessons
CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- User Progress
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    UNIQUE(user_id, lesson_id)
);

-- Enrollments
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, course_id)
);
```

---

## Development Workflow

### Common Commands

```bash
# Run development server
python manage.py runserver

# Create new app
python manage.py startapp <app_name>

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

### Git Workflow

```bash
# Check status
git status

# Current branch
git branch
# Output: changes/code-base-context

# Main branch
# Use 'main' for pull requests

# Stage changes
git add <file>

# Commit changes
git commit -m "Description"

# Push changes
git push origin changes/code-base-context
```

---

## Troubleshooting

### Issue: "No module named 'environ'"

**Solution**:
```bash
pip install environ
```

### Issue: Database connection error

**Solution**:
1. Check PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify database exists: `psql -U postgres -l`
3. Check credentials in `.env` file
4. Ensure database host is correct (usually `localhost`)

### Issue: Static files not loading

**Solution**:
```bash
# Development
python manage.py collectstatic

# Check STATIC_URL in settings.py
# Verify STATICFILES_DIRS path is correct
```

### Issue: Activation email not sending

**Solution**:
1. Check console/terminal for email output (console backend is active)
2. For SMTP: Verify email credentials in `.env`
3. For Gmail: Use App Password instead of regular password
4. Enable "Less secure app access" in Gmail settings (if needed)

### Issue: CSRF token missing or incorrect

**Solution**:
1. Ensure `{% csrf_token %}` is in all POST forms
2. Check `django.middleware.csrf.CsrfViewMiddleware` is in MIDDLEWARE
3. For AJAX: Use CSRF-exempt views or pass token in headers

---

## Contributing

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions small and focused

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request to the `main` branch

---

## License

[Add your license information here]

---

## Contact & Support

For questions, issues, or contributions:

- **Repository**: [Add repository URL]
- **Issues**: [Add issues URL]
- **Documentation**: This README

---

## Acknowledgments

- Django documentation: https://docs.djangoproject.com/
- Bootstrap: https://getbootstrap.com/
- jQuery: https://jquery.com/
- Feather Icons: https://feathericons.com/

---

**Last Updated**: October 13, 2025
**Version**: 1.0.0
**Django Version**: 5.2.7
**Python Version**: 3.12+
