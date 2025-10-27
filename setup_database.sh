#!/bin/bash
# Database Setup Script for Classes Application

echo "Setting up PostgreSQL database for Classes application..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if PostgreSQL is running
if ! systemctl is-active --quiet postgresql; then
    echo -e "${YELLOW}Starting PostgreSQL service...${NC}"
    sudo systemctl start postgresql
fi

# Create database and user
echo -e "${YELLOW}Creating database and user...${NC}"
sudo -u postgres psql << EOF
-- Create database if it doesn't exist
SELECT 'CREATE DATABASE classes_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'classes_db')\gexec

-- Create user if it doesn't exist
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'postgres') THEN
    CREATE USER postgres WITH PASSWORD 'postgres';
  END IF;
END
\$\$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE classes_db TO postgres;
ALTER USER postgres WITH SUPERUSER;

\q
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database setup completed successfully!${NC}"
else
    echo -e "${RED}✗ Database setup failed. Please run manually:${NC}"
    echo "sudo -u postgres createdb classes_db"
fi

# Run migrations
echo -e "${YELLOW}Running Django migrations...${NC}"
source .venv/bin/activate
python manage.py migrate

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migrations completed successfully!${NC}"
else
    echo -e "${RED}✗ Migrations failed.${NC}"
    exit 1
fi

# Create superuser prompt
echo ""
echo -e "${YELLOW}Would you like to create a superuser? (y/n)${NC}"
read -p "Answer: " create_superuser

if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "You can now run the application with:"
echo "  ./start_server.sh"
echo ""
echo "Or manually with:"
echo "  .venv/bin/daphne -b 0.0.0.0 -p 8000 classes.asgi:application"
