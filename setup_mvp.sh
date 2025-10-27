#!/bin/bash

# Ctrl+Shift Academy MVP Setup Script
# This script sets up the MVP version of the application

echo "========================================="
echo "  Ctrl+Shift Academy - MVP Setup"
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Check database connection
echo ""
echo "🔍 Checking database configuration..."
if ! python3 manage.py check --database default > /dev/null 2>&1; then
    echo "❌ Database connection failed!"
    echo "Please ensure PostgreSQL is running and .env file is configured correctly."
    exit 1
fi
echo "✓ Database connection successful"

# Create migrations
echo ""
echo "🔨 Creating database migrations..."
python3 manage.py makemigrations

# Run migrations
echo ""
echo "🚀 Applying database migrations..."
python3 manage.py migrate

# Create superuser if needed
echo ""
read -p "Do you want to create a superuser? (y/n): " create_superuser
if [ "$create_superuser" = "y" ]; then
    python3 manage.py createsuperuser
fi

# Seed database
echo ""
read -p "Do you want to seed the database with sample courses? (y/n): " seed_db
if [ "$seed_db" = "y" ]; then
    echo "🌱 Seeding database with sample data..."
    python3 manage.py seed_data
fi

echo ""
echo "========================================="
echo "  ✓ MVP Setup Complete!"
echo "========================================="
echo ""
echo "📋 Next Steps:"
echo "  1. Run: python3 manage.py runserver"
echo "  2. Visit: http://127.0.0.1:8000/"
echo "  3. Login with your credentials"
echo ""
echo "🔑 Admin Panel: http://127.0.0.1:8000/admin/"
if [ "$seed_db" = "y" ]; then
    echo ""
    echo "📚 Sample Instructor Account:"
    echo "  Username: instructor"
    echo "  Password: instructor123"
fi
echo ""
echo "Happy coding! 🎓"
