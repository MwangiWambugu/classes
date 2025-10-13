#!/bin/bash

# Ctrl+Shift Academy Phase 2 Setup Script
# Implements: Progress Tracking, Enrollment, Profiles, Quizzes, Certificates

echo "========================================="
echo "  Ctrl+Shift Academy - Phase 2 Setup"
echo "========================================="
echo ""
echo "Phase 2 Features:"
echo "  ✓ User Progress Tracking"
echo "  ✓ Course Enrollment System"
echo "  ✓ User Profiles & Avatars"
echo "  ✓ Course Categories & Search"
echo "  ✓ Completion Certificates"
echo "  ✓ Quiz System"
echo "  ✓ Instructor Dashboard"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Please run ./setup_mvp.sh first"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Create migrations
echo ""
echo "🔨 Creating database migrations for Phase 2 models..."
python3 manage.py makemigrations

if [ $? -ne 0 ]; then
    echo "❌ Migration creation failed!"
    exit 1
fi

# Run migrations
echo ""
echo "🚀 Applying database migrations..."
python3 manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Migration failed!"
    exit 1
fi

echo ""
echo "========================================="
echo "  ✓ Phase 2 Setup Complete!"
echo "========================================="
echo ""
echo "📋 Phase 2 Features Now Available:"
echo ""
echo "  For Students:"
echo "    • Course enrollment system"
echo "    • Progress tracking (lessons completed)"
echo "    • User profiles with statistics"
echo "    • Course search & filtering"
echo "    • Completion certificates"
echo "    • Lesson quizzes"
echo ""
echo "  For Instructors:"
echo "    • Instructor dashboard with analytics"
echo "    • Student progress tracking"
echo "    • Quiz creation & management"
echo ""
echo "📋 Next Steps:"
echo "  1. Run: python3 manage.py runserver"
echo "  2. Visit: http://127.0.0.1:8000/"
echo "  3. Enroll in a course"
echo "  4. Complete lessons and earn certificates!"
echo ""
echo "🔗 New URLs Available:"
echo "  • /my-courses/ - View enrolled courses"
echo "  • /profile/ - Your profile page"
echo "  • /instructor/dashboard/ - Instructor analytics"
echo ""
echo "📖 For detailed documentation, see PHASE2_IMPLEMENTATION.md"
echo ""
echo "Happy Learning! 🎓"
