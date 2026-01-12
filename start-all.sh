#!/bin/bash

# AI Disease Detection Platform - Linux/Mac Startup Script
# This script starts both frontend and backend services

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "AI Disease Detection Platform"
echo "Starting Frontend and Backend Services"
echo "========================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3 && ! command_exists python; then
    echo -e "${RED}[ERROR]${NC} Python is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/downloads/"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command_exists python3; then
    PYTHON_CMD="python"
fi

# Check if Node.js is installed
if ! command_exists node; then
    echo -e "${RED}[ERROR]${NC} Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo -e "${BLUE}[1/5]${NC} Checking backend dependencies..."
cd ai-backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! $PYTHON_CMD -c "import fastapi" 2>/dev/null; then
    echo "Installing backend dependencies... (this may take 5-10 minutes)"
    pip install -r requirements.txt
fi

echo ""
echo -e "${BLUE}[2/5]${NC} Checking frontend dependencies..."
cd ../ai-disease-ui

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies... (this may take 3-5 minutes)"
    npm install
fi

echo ""
echo -e "${BLUE}[3/5]${NC} Starting Backend Server..."
cd ../ai-backend

# Create log directory
mkdir -p logs

# Start backend in background
source venv/bin/activate
nohup $PYTHON_CMD -m app.main > logs/backend.log 2>&1 &
BACKEND_PID=$!

echo -e "${GREEN}✓${NC} Backend started (PID: $BACKEND_PID)"
echo "  Log file: ai-backend/logs/backend.log"

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 10

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${RED}[ERROR]${NC} Backend failed to start. Check logs/backend.log"
    exit 1
fi

echo ""
echo -e "${BLUE}[4/5]${NC} Starting Frontend Server..."
cd ../ai-disease-ui

# Start frontend in background
nohup npm run dev > ../ai-backend/logs/frontend.log 2>&1 &
FRONTEND_PID=$!

echo -e "${GREEN}✓${NC} Frontend started (PID: $FRONTEND_PID)"
echo "  Log file: ai-backend/logs/frontend.log"

# Wait for frontend to start
echo "Waiting for frontend to initialize..."
sleep 8

# Check if frontend is running
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${RED}[ERROR]${NC} Frontend failed to start. Check logs/frontend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo -e "${BLUE}[5/5]${NC} Opening application in browser..."

# Open browser (cross-platform)
if command_exists xdg-open; then
    xdg-open http://localhost:3000 2>/dev/null &
elif command_exists open; then
    open http://localhost:3000 2>/dev/null &
elif command_exists start; then
    start http://localhost:3000 2>/dev/null &
fi

# Save PIDs to file for easy stopping
cd ..
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo ""
echo "========================================"
echo -e "${GREEN}Successfully Started!${NC}"
echo "========================================"
echo ""
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}Backend:${NC}  http://localhost:8000"
echo -e "${GREEN}API Docs:${NC} http://localhost:8000/docs"
echo ""
echo "Process IDs:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "Logs:"
echo "  Backend:  ai-backend/logs/backend.log"
echo "  Frontend: ai-backend/logs/frontend.log"
echo ""
echo "To view logs in real-time:"
echo "  Backend:  tail -f ai-backend/logs/backend.log"
echo "  Frontend: tail -f ai-backend/logs/frontend.log"
echo ""
echo "To stop the servers, run:"
echo "  ./stop-all.sh"
echo ""
echo -e "${YELLOW}Note:${NC} Services are running in the background."
echo "      This terminal can be closed safely."
echo ""
