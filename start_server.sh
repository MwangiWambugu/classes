#!/bin/bash
# Start script for Classes Application with WebSocket support

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}   Classes Application Server${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check if virtual environment is set up
if [ ! -d ".venv" ]; then
    echo -e "${RED}✗ Virtual environment not found!${NC}"
    echo "Please run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if Redis is running
if ! pgrep -x redis-server > /dev/null; then
    echo -e "${YELLOW}⚠ Redis is not running. WebSocket features require Redis.${NC}"
    echo -e "${YELLOW}  Start Redis with: sudo systemctl start redis${NC}"
    echo ""
fi

# Check if database exists
export PGPASSWORD='@K1m3m14'
if ! psql -h localhost -U kimemia -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw classes_db; then
    echo -e "${RED}✗ Database 'classes_db' not found!${NC}"
    echo "Please run: ./setup_database.sh"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo -e "${GREEN}✓ Starting application server...${NC}"
echo ""
echo -e "${YELLOW}Server will be available at:${NC}"
echo "  → HTTP: http://localhost:8000"
echo "  → WebSocket: ws://localhost:8000/ws/chat/"
echo ""
echo -e "${YELLOW}Available URLs:${NC}"
echo "  → Home/Lessons:     http://localhost:8000/"
echo "  → Chat:             http://localhost:8000/chat/"
echo "  → Authentication:   http://localhost:8000/authentication/login/"
echo "  → Admin Panel:      http://localhost:8000/admin/"
echo ""
echo -e "${CYAN}Press Ctrl+C to stop the server${NC}"
echo ""

# Start Daphne ASGI server for WebSocket support
exec .venv/bin/daphne -b 0.0.0.0 -p 8000 classes.asgi:application
