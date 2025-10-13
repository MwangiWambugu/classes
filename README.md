# Ctrl+Shift Academy Platform

  Developer-facing documentation for the Django project in `/var/www/html/contract/mwangi_jeremiah/classes`.

  ## Overview
  Ctrl+Shift Academy is a Django 5.2 application that prototypes a gated “lessons” dashboard. Users self-register, confirm their accounts via an email activation link, sign in, and then gain
  access to the lessons area. The codebase currently focuses on authentication and layout scaffolding; domain-specific lesson data has not yet been modeled.

  ## Architecture

  | Layer | Responsibility | Key Modules |
  |-------|----------------|-------------|
  | Project configuration | Settings, global URLs, WSGI/ASGI bootstrap | `classes/settings.py`, `classes/urls.py`, `manage.py` |
  | Authentication app | Registration, login, logout, activation, AJAX field validation | `authentication/views.py`, `authentication/urls.py`, `authentication/utils.py` |
  | Lessons app | Auth-protected dashboard landing page | `lessons/views.py`, `lessons/urls.py` |
  | Presentation | Shared layouts, auth forms, dashboard shell, static assets | `templates/`, `classes/static/` |

  ### Directory Layout

  classes/                 # Django project package (settings, static files)
  authentication/          # Auth app (class-based views, token helpers)
  lessons/                 # Lessons app (simple login-required view)
  templates/               # HTML templates (base layouts & partials)
  classes/static/          # Compiled CSS/JS bundled with the project
  py312/                   # Existing local virtual environment (optional)
  requirements.txt         # Python dependencies (Django, Postgres client, etc.)
  manage.py                # Django management entrypoint


  ## Request & Business Flow


  GET /               --> lessons.urls --> lessons.views.home  (requires login)
  GET /authentication/register/ --> registrationView.get()
  POST /authentication/register/ --> registrationView.post()
  • Validates username/email uniqueness.
  • Persists inactive user; emails activation link.
  GET /authentication/activate/<uid>/<token>/ --> verificationView.get()
  • Confirms token; flips user.is_active; redirects to login.
  GET /authentication/login/ --> loginView.get()
  POST /authentication/login/ --> loginView.post()
  • Authenticates active users; redirects to / (lessons dashboard).
  POST /authentication/logout/ --> logoutView.post()


  Supporting AJAX endpoints (CSRF-exempt) provide real-time validation during sign-up:
  - `POST /authentication/validate_username/`
  - `POST /authentication/validate_email/`

  `authentication/utils.py` defines `appTokenGenerator`, extending Django’s password-reset token generator to include `user.is_active` in the hash. This invalidates links once an account has
  been activated.

  `lessons/views.py` wraps the dashboard with `@login_required(login_url='/authentication/login/')`, enforcing authentication before any lesson content renders.

  ## Templates & Front-End

  - `templates/base.html` – Authenticated layout with sidebar and top nav; expects `logout` form submission.
  - `templates/base_auth.html` – Minimal shell for login/register pages.
  - `templates/authentication/*.html` – Standard Bootstrap forms consuming Django messages and static JS (`register.js`) for AJAX validation and password toggle.
  - `templates/partials/_messages.html` – Renders Django flash messages using Bootstrap alerts.
  - `templates/partials/_sidebar.html` – Placeholder navigation items for dashboard sections.
  - `classes/static/js/register.js` – Handles username/email validation and password visibility toggle.
  - `classes/static/css/main.css`, `dashboard.css`, `bootstrap.min.css` – Styling assets bundled locally.

  > **Heads-up:** `register.js` currently calls `/authentication/validate-email/` and `/authentication/validate-username/` (hyphenated), but the server is wired for underscore paths. Update
  the JS or URL patterns before relying on AJAX validation. Additional feedback containers referenced in JS (`.email-invalid-feedback`, `.password-invalid-feedback`) are not present in the
  templates yet.

  ## Configuration

  `classes/settings.py` pulls connection details from `.env`:

  | Variable | Purpose |
  |----------|---------|
  | `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` | PostgreSQL database configuration |
  | `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials for activation emails |

  The email backend defaults to `django.core.mail.backends.console.EmailBackend`, so activation links appear in the server logs/console unless you override this in the environment.

  Static files are collected from `classes/static` via `STATICFILES_DIRS`, with `STATIC_ROOT` pointing to `<BASE_DIR>/static` for deploy-time collection.

  ## Local Setup

  1. **Python environment**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate  # or use existing py312/ if desired

  2. Install dependencies

     pip install -r requirements.txt
  3. PostgreSQL & environment
      - Provision a Postgres database.
      - Create a .env in the project root:

        DB_NAME=ctrlshift
        DB_USER=ctrlshift_user
        DB_PASSWORD=changeme
        DB_HOST=127.0.0.1
        EMAIL_HOST=smtp.example.com
        EMAIL_HOST_USER=notifications@example.com
        EMAIL_HOST_PASSWORD=super-secret
  4. Migrate & bootstrap

     python manage.py migrate
     python manage.py createsuperuser
  5. Run the server

     python manage.py runserver
     Visit http://127.0.0.1:8000/ to load the lessons dashboard (after logging in).

  ## Testing & Quality

  - No automated tests are defined yet (authentication/tests.py, lessons/tests.py are placeholders).
  - You can run Django’s default test runner once tests are added:

    python manage.py test

  ## Known Issues & To-Do

  - AJAX validation endpoints: JavaScript uses hyphenated URLs that return 404 against current server routes.
  - Logout method: templates/base.html submits the logout form without method="post", so the view redirects rather than logging out. Add method="post" and a CSRF token to align with
    logoutView.
  - Email delivery: Console backend is fine for development but must be swapped for SMTP or a transactional service in production.
  - Password feedback: Front-end references feedback containers/classes not present in the HTML, so validation messages never display.
  - Lessons domain: No models or lesson content exist yet; lessons/index.html is currently empty.

  * Update the README as features evolve (e.g., once lesson models, APIs, or additional dashboards are implemented).


  - Suggested next steps:
    1. Fix the AJAX endpoint path mismatches in `classes/static/js/register.js`.
    2. Add `method="post"` (plus CSRF token) to the logout form in `templates/base.html`.
    3. Decide on actual lesson data models and seed content to demonstrate the dashboard.
    4. Replace the console email backend and document SMTP requirements once ready for staging/production.