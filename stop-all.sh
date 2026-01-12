#!/bin/bash

# AI Disease Detection Platform - Linux/Mac Stop Script

echo "========================================"
echo "Stopping AI Disease Detection Platform"
echo "========================================"
echo ""

# Check for saved PIDs
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    rm .backend.pid
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    rm .frontend.pid
fi

# Also try to kill by port
echo "Checking for processes on ports 3000 and 8000..."

# Kill process on port 8000
if command -v lsof >/dev/null 2>&1; then
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
fi

echo ""
echo "========================================"
echo "All servers stopped!"
echo "========================================"
echo ""
